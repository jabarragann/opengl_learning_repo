import numpy as np
from numpy.core.numeric import indices 
import pandas as pd
from numpy import cos, sin

PI = np.pi

if __name__ == "__main__":
    vertices_df = pd.DataFrame(columns=['x','y','z']) 

    sectorCount = 4 
    stackCount = 4        
    radius = 0.5 

    # float x, y, z, xy;                              // vertex position
    # float nx, ny, nz, lengthInv = 1.0f / radius;    // vertex normal
    # float s, t;                                     // vertex texCoord

    sectorStep = 2 * PI / sectorCount
    stackStep = PI / stackCount
    sectorAngle=0
    stackAngle = 0

    for i in range(stackCount+1):
        stackAngle = PI / 2 - i * stackStep;        # starting from pi/2 to -pi/2
        xy = radius * cos(stackAngle);              # r * cos(u)
        z = radius * sin(stackAngle);               # r * sin(u)

        # add (sectorCount+1) vertices per stack
        # the first and last vertices have same position and normal, but different tex coords
        for j in range(sectorCount+1):
            sectorAngle = j * sectorStep;           #starting from 0 to 2pi

            # vertex position (x, y, z)
            x = xy * cos(sectorAngle);             # r * cos(u) * cos(v)
            y = xy * sin(sectorAngle);             # r * cos(u) * sin(v)

            vertices_df = vertices_df.append(pd.DataFrame([[x,y,z]],columns=['x','y','z']),ignore_index=True)

            # vertices.push_back(x);
            # vertices.push_back(y);
            # vertices.push_back(z);

            # // normalized vertex normal (nx, ny, nz)
            # nx = x * lengthInv;
            # ny = y * lengthInv;
            # nz = z * lengthInv;
            # normals.push_back(nx);
            # normals.push_back(ny);
            # normals.push_back(nz);

            # // vertex tex coord (s, t) range between [0, 1]
            # s = (float)j / sectorCount;
            # t = (float)i / stackCount;
            # texCoords.push_back(s);
            # texCoords.push_back(t);
    #print(vertices_df)
    vertices_df.to_csv("sphere_vertices.csv", index=None)

    indices_df = pd.DataFrame(columns=['id1','id2','id3'])
    #Create Mesh triangles
    for i in range(stackCount):
        k1 = i * (sectorCount + 1);     # beginning of current stack
        k2 = k1 + sectorCount + 1;      # beginning of next stack

        for j in range(sectorCount):
            # 2 triangles per sector excluding first and last stacks
            # k1 => k2 => k1+1
            if i != 0:
                indices_df = indices_df.append(pd.DataFrame([[k1,k2,k1+1]],columns=['id1','id2','id3']))
            # k1+1 => k2 => k2+1
            if i != (stackCount-1):
                indices_df = indices_df.append(pd.DataFrame([[k1+1,k2,k2+1]],columns=['id1','id2','id3']))

            k1+=1
            k2+=1

    indices_df.to_csv('sphere_indices.csv',index=None)
    
    