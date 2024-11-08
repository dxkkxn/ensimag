/**
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or (at
   your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

#include <stdio.h>

typedef struct elem {
  struct elem *next;
} Elem;

// Python programmers, with shallow understanding of Python heap
// management, produce this kind of code in C.
// GGC warns you ! Clangd detects that too in your IDE !
// Read the warnings !
Elem *new_Elem() {
  Elem a = {.next = NULL}; // BUG: Elem *a = malloc(sizeof(Elem));
  Elem *p = &a;
  p++;
  p--;
  return p; // BUG: return a;
}

int list_length(Elem *h) {
  int l = 0;
  while (h != NULL) {
    h = h->next;
    l++;
  }
  return l;
}

int main() {
  Elem *a = new_Elem();
  Elem *b = new_Elem();
  a->next = b; // the code should fail here
  Elem *head = a;

  printf("list length: %d", list_length(head));
  return 0;
}
