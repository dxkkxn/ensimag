/*******************************************************************************
 * vim:set ts=3:
 * File   : screen.c, file for JPEG-JFIF sequential decoder    
 *
 * Copyright (C) 2007 TIMA Laboratory
 * Author(s) :      Patrice, GERIN patrice.gerin@imag.fr
 * Bug Fixer(s) :   Xavier, GUERIN xavier.guerin@imag.fr
 * 					  Pierre-Henri HORREIN pierre-henri.horrein@imag.fr
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 *
 ******************************************************************************/
#include "stdio.h"
#include "stdlib.h"
#include "x86intrin.h"
#include "SDL2/SDL.h"
#include "define_common.h"

static SDL_Window *screen;
static SDL_Surface *image;
static SDL_Renderer *renderer;
static SDL_Texture *texture;
// Frame rate management, stores previous counter value
static int old_time ;
// According to when the quit event is detected, the player can get stuck
// the "initialized" parameter prevents this
static int initialized ;


void screen_init(uint32_t width, uint32_t height)
{

	int width_int = width , height_int = height ;
   /* Initialize defaults, Video and Audio */
   if (SDL_Init(SDL_INIT_VIDEO) < 0) { 
      printf("Could not initialize SDL: %s.\n", SDL_GetError());
      exit(-1);
   }

   /* Clean up on exit */
   atexit(SDL_Quit);

   screen = SDL_CreateWindow("The Difficult Life of Scart",
                                          SDL_WINDOWPOS_UNDEFINED,
                                          SDL_WINDOWPOS_UNDEFINED,
                                          width, height, 0);
   if (screen == NULL) {
      fprintf(stderr, "Couldn't create %ux%u window: %s\n",
              width, height, SDL_GetError());
      exit(1);
   }

   renderer = SDL_CreateRenderer(screen, -1, 0);

   if (renderer == NULL) {
      fprintf(stderr, "Couldn't create renderer: %s\n", SDL_GetError());
      exit(1);
   }

	if ((width % 8) != 0) {
		width_int = ((width / 8) + 1) * 8 ;
	}
	if ((height % 8) != 0) {
		height_int = ((height / 8) + 1) * 8 ;
	}

   texture = SDL_CreateTexture(renderer,
                               SDL_PIXELFORMAT_RGBA8888,
                               SDL_TEXTUREACCESS_TARGET,
                               width_int, height_int);

   if (texture == NULL) {
       fprintf(stderr, "Couldn't create texture: %s\n", SDL_GetError());
       exit(1);
   }

   uint32_t rmask, gmask, bmask, amask;

#if 1 // SDL_BYTEORDER == SDL_BIG_ENDIAN
   rmask = 0x00ff0000;
   gmask = 0x0000ff00;
   bmask = 0x000000ff;
   amask = 0x00000000;
#else
   rmask = 0x000000ff;
   gmask = 0x0000ff00;
   bmask = 0x00ff0000;
   amask = 0xff000000;
#endif
   image = SDL_CreateRGBSurface(SDL_SWSURFACE, width_int, height_int, 32,
                                rmask, gmask, bmask, amask);

   if (texture == NULL) {
      fprintf(stderr, "Couldn't create surface: %s\n", SDL_GetError());
      exit(1);
   }
	old_time = SDL_GetTicks() ;
	initialized	= 1 ;
}

int screen_exit()
{
    /* Shutdown all subsystems */
    SDL_Event event ;
    while(initialized) {
        SDL_PollEvent(&event) ;
        if ((event.type == SDL_QUIT )) {
            SDL_DestroyTexture(texture);
            SDL_FreeSurface(image);
            SDL_DestroyRenderer(renderer);
            SDL_DestroyWindow(screen);
            SDL_Quit();
            return 1;
        }
    }
    return 0 ;
}

void screen_cpyrect(uint32_t x, uint32_t y, uint32_t w, uint32_t h, void *ptr)
{
   void *dest_ptr;
   void *src_ptr;
   uint32_t line;
   
   SDL_LockSurface(image);

   for(line = 0; line < h ; line++)
   {
      dest_ptr = (void*)((uintptr_t)image->pixels + (((x+line)*image->w + y) << 2));
      src_ptr = (void*)((uintptr_t)ptr + ((line * w) << 2));
      memcpy(dest_ptr,src_ptr,w << 2);
   }

   SDL_UnlockSurface(image);
}

int screen_refresh() 
{
	uint64_t new_time;
	static uint64_t finish_clock, old_clock ;
	SDL_Event event ;
	new_time = SDL_GetTicks() ;
	finish_clock = _rdtsc() ;

	while (new_time - old_time < 1000 / 25) {
		new_time = SDL_GetTicks() ;
	}

   texture = SDL_CreateTextureFromSurface(renderer, image);
   SDL_RenderCopy(renderer, texture, NULL, NULL);
   SDL_RenderPresent(renderer);

	IPRINTF("[screen]: instantaneous fps is %0.2f\n", 1000.00f / (SDL_GetTicks() - old_time)) ;
	printf("[screen] : framerate is %0.2ffps, computed one image in %lu clock cycles\n", 1000.00f / (SDL_GetTicks() - old_time), finish_clock - old_clock) ;
	old_time = SDL_GetTicks() ;
	old_clock = _rdtsc() ;
	// In this case, SDL is 
	if(SDL_PollEvent(&event)) {
		if (event.type == SDL_QUIT) {
			initialized = 0 ;
			SDL_Quit();
			return 1 ;
		}
	}
	return 0 ;
}
