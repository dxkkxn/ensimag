import OpenGL.GL as GL              # standard Python OpenGL wrapper
from PIL import Image               # load texture maps
from core import Viewer

# -------------- OpenGL Texture Wrapper ---------------------------------------
class Texture:
    """ Helper class to create and automatically destroy textures """
    def __init__(self, tex_file=None, wrap_mode=GL.GL_REPEAT,
                 mag_filter=GL.GL_LINEAR, min_filter=GL.GL_LINEAR_MIPMAP_LINEAR,
                 tex_type=GL.GL_TEXTURE_2D):
        self.type = tex_type
        if (tex_file!=None):
            self.glid = GL.glGenTextures(1)
        
            try:
                # imports image as a numpy array in exactly right format
                
                tex = Image.open(tex_file).convert('RGBA')
                GL.glBindTexture(tex_type, self.glid)
                GL.glTexImage2D(tex_type, 0, GL.GL_RGBA, tex.width, tex.height,
                                0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex.tobytes())
                GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_S, wrap_mode)
                GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_T, wrap_mode)
                GL.glTexParameteri(tex_type, GL.GL_TEXTURE_MIN_FILTER, min_filter)
                GL.glTexParameteri(tex_type, GL.GL_TEXTURE_MAG_FILTER, mag_filter)
                GL.glGenerateMipmap(tex_type)
                print(f'Loaded texture {tex_file} ({tex.width}x{tex.height}'
                    f' wrap={str(wrap_mode).split()[0]}'
                    f' min={str(min_filter).split()[0]}'
                    f' mag={str(mag_filter).split()[0]})')
            except FileNotFoundError:
                print("ERROR: unable to load texture file %s" % tex_file)

    def __del__(self):  # delete GL texture from GPU when object dies
        GL.glDeleteTextures(self.glid)



# -------------- Textured mesh decorator --------------------------------------
class Textured:
    """ Drawable mesh decorator that activates and binds OpenGL textures """
    def __init__(self, drawable, **textures):
        self.drawable = drawable
        self.textures = textures
        # self.textures.diffuse_map = "nouvel attribut"
        # print("selfTex", self.textures)
        self.requireFB = False

    def doesRequireFB(self):
        return self.requireFB

    def setRequireFB(self, bool):
        self.requireFB = bool

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        for index, (name, texture) in enumerate(self.textures.items()):
            GL.glActiveTexture(GL.GL_TEXTURE0 + index)
            if(self.doesRequireFB()):
                if (index==0):
                    GL.glBindTexture(texture.type, Viewer.water_reflex)
                elif (index==1):
                    GL.glBindTexture(texture.type, Viewer.water_refrac)
                elif (index==4):
                    GL.glBindTexture(texture.type, Viewer.water_depth)
            else:
                GL.glBindTexture(texture.type, texture.glid)
            uniforms[name] = index
        self.drawable.draw(primitives=primitives, **uniforms)
