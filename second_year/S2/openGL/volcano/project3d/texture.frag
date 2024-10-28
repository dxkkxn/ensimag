#version 330 core

uniform sampler2D herbe_map;
uniform sampler2D rock_map;
uniform sampler2D sand_map;
uniform sampler2D rock_normal;
uniform vec3 light_dir;

// in vec3 normal;
// in vec2 gfrag_tex_coords;

in vec3 normal_position;
in vec3 tangent_position;

in vec2 frag_tex_coords;
in float distance_gradiant;
in vec3 camera_direction;
in mat4 model_matrix;

out vec4 out_color;


void main() {
    float t_volcan = clamp((10-distance_gradiant) / 10, 0.0, 1.0);
    float t_sable = clamp((distance_gradiant-8) / 8, 0.0, 1.0);
    float interpolation_volcan = smoothstep(0.0,1.0,t_volcan);
    float interpolation_sable = smoothstep(0.0,1.0,t_sable);   

    vec3 bitangent_position = cross(tangent_position, normal_position);

    vec3 relief = (texture(rock_normal, frag_tex_coords)).rgb * 2.0 - 1.0;

    //vec3 relief_normal = (model_matrix * vec4(vec3(relief.y, relief.z, relief.x), 0.0)).xyz;

    vec3 relief_normal = relief.r * tangent_position + relief.g * bitangent_position + relief.b * normal_position;

    vec4 textured = mix(texture(herbe_map, frag_tex_coords), texture(rock_map, frag_tex_coords), interpolation_volcan);
    textured= mix(textured, texture(sand_map, frag_tex_coords), interpolation_sable);

    

    float diffuse = max(0.0, dot(light_dir, normal_position)) + interpolation_volcan*max(0.0, dot(light_dir, relief_normal));
    float specular = interpolation_volcan*(max(0.0, dot(camera_direction, normalize(reflect(light_dir, normal_position))))+max(0.0, dot(camera_direction, normalize(reflect(light_dir, relief_normal)))));
    float factor = diffuse;//(0.75*diffuse+0.25*specular);

    out_color = vec4(factor * textured.xyz, 1.0);
}
