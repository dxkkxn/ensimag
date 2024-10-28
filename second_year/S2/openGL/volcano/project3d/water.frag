#version 400 core

uniform sampler2D reflex_map;
uniform sampler2D refrac_map;
uniform sampler2D dudv_map;
uniform sampler2D normal_map;
uniform sampler2D depth_map;
uniform vec3 light_dir;
uniform float moveFactor;


in vec4 clipSpace;
in vec3 toCameraVector;
in vec2 textureCoords;

out vec4 out_color;

const float waveStrength = 0.02;
const float shineDamper = 20.0;
const float reflectivity = 0.6;


void main(void) {
	
		vec2 ndc = (clipSpace.xy/clipSpace.w)/2.0 +0.5;
		vec2 refractTexCoords = vec2(ndc.x, ndc.y);
		vec2 reflectTexCoords = vec2(ndc.x, -ndc.y);

		float near = 0.1;
		float far = 10.0;
		float depth = texture(depth_map, refractTexCoords).r;
		float floorDistance = 2.0 * near * far / (far + near - (2.0*depth - 1.0) * (far-near));
		
		depth = gl_FragCoord.z;
		float waterDistance = 2.0 * near * far / (far + near - (2.0*depth - 1.0) * (far-near));
		float waterDepth = floorDistance-waterDistance;

		vec2 distortedTexCoords = texture(dudv_map, vec2(textureCoords.x + moveFactor, textureCoords.y)).rg*0.1;
		distortedTexCoords = textureCoords + vec2(distortedTexCoords.x, distortedTexCoords.y+moveFactor);
		vec2 totalDistortion = (texture(dudv_map, distortedTexCoords).rg * 2.0 - 1.0) * waveStrength;

		refractTexCoords +=totalDistortion;
		refractTexCoords = clamp(refractTexCoords, 0.001,0.999);

		reflectTexCoords += totalDistortion;
		reflectTexCoords.x = clamp(reflectTexCoords.x, 0.001, 0.999);
		reflectTexCoords.y = clamp(reflectTexCoords.y, -0.999, -0.001);


		vec4 refraction = texture(refrac_map, refractTexCoords);
		vec4 reflection = texture(reflex_map, reflectTexCoords);

		vec3 viewVector = normalize(toCameraVector);
		float refractiveFactor = dot(viewVector, vec3(0.0,0.0,1.0));
		refractiveFactor = pow(refractiveFactor, 0.5);
		refractiveFactor = clamp(refractiveFactor, 0.0, 1.0);

		vec4 normalMapColour= texture(normal_map, distortedTexCoords);
		vec3 normal = vec3(normalMapColour.r * 2.0 - 1.0, normalMapColour.b, normalMapColour.g * 2.0 -1.0);
		normal = normalize(normal);

		vec3 reflectedLight = reflect(normalize(light_dir), normal);
		float specular = max(dot(reflectedLight, viewVector), 0.0);
		specular = pow(specular, shineDamper);
		vec3 specularHighlights = vec3(1,1,1) * specular *reflectivity;
		
	
		out_color = mix(reflection, refraction, refractiveFactor);
		out_color= mix(out_color, vec4(0.0, 0.1, 0.06,1.0), 0.2) + vec4(specularHighlights, 0.0);
}