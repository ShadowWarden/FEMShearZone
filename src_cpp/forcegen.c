/* forcegen.c
 * Omkar H. Ramachandran
 * omkar.ramachandran@colorado.edu
 *
 *
 * Computes Force on the nodes of a node due to a singluar element
 */

#include <stdio.h>
#include <stdlib.h>

struct Elem{
	int n[3];
	float E;
	float nu;
};

float * dot(float * A, int m1, int n1, float * B, int m2,int n2,int transpose){
	// Assume n1=m2. Not my problem if you screw up
	int i,j,k;
	float * C = (float *) malloc (sizeof(float)*m1*n2);

	for(i=0;i<m1;i++)
		for(j=0;j<n2;j++)
			C[i*n2+j] = 0;

	for(i=0;i<m1;i++){
		for(j=0;j<n2;j++){
			for(k=0;k<n1;k++){
				C[n2*i+j] += A[n1*i+k]*B[n2*k+j];
			}
		}
	}

	return C;	
}

void GenForce(float * Fx, float * Fy, struct Elem * E, float * x, float * y, int num_elem, float * vx, float * vy){
/* Generate internal material forces on nodes
 */
//	int i = blockIdx.x*1024 + threadIdx.x;

//	if(i >= num_elem)
//		return;

	int i = 0;

	// Get sides from Triangle
	float x12 = x[E[i].n[0]] - x[E[i].n[1]];
	float x13 = x[E[i].n[0]] - x[E[i].n[2]];
	float x23 = x[E[i].n[1]] - x[E[i].n[2]];
	float y12 = y[E[i].n[0]] - y[E[i].n[1]];
	float y13 = y[E[i].n[0]] - y[E[i].n[2]];
	float y23 = y[E[i].n[1]] - y[E[i].n[2]];

	// Find triangle area
	float det = x13*y23-x23*y13;

	// Compute Shape function
	float B[18] = {y23/det,0,-y13/det,0,y12/det,0,0,-x23/det,0,x13/det,0,-x12/det,-x23/det,y23/det,x13/det,-y13/det,-x12/det,y12/det};

	float Bt[18];
	int j,k;
	for(j=0;j<6;j++)
		for(k=0;k<3;k++)
			Bt[3*j+k] = B[6*k+j];

	float cofactor = E[i].E/(1-E[i].nu-2*E[i].nu*E[i].nu);
	float D[9] = {cofactor*(1-E[i].nu),cofactor*E[i].nu,0,cofactor*E[i].nu,cofactor*(1-E[i].nu),0,0,0,0.5*(1-2*E[i].nu)};

	// Compute B^{T}DB
	float * interm = dot(Bt,6,3,D,3,3,1);
	float * K = dot(interm,6,3,B,3,6,0);

	free(interm);
	
	float V[6] = {vx[E[i].n[0]],vy[E[i].n[0]],vx[E[i].n[1]],vy[E[i].n[1]],vx[E[i].n[2]],vy[E[i].n[2]]};

	float * Flocal = dot(K,6,6,V,6,1,0);

	Fx[E[i].n[0]] += Flocal[0];
	Fy[E[i].n[0]] += Flocal[1];
	Fx[E[i].n[1]] += Flocal[2];
	Fy[E[i].n[1]] += Flocal[3];
	Fx[E[i].n[2]] += Flocal[4];
	Fy[E[i].n[2]] += Flocal[5];

	free(Flocal);
	free(K);
}

int main(int argc, char ** argv){
	int i;

	float Fx[3] = {0,0,0};
	float Fy[3] = {0,0,0};
	float *dev_Fx, *dev_Fy;

	float x[3] = {0,1,0};
	float y[3] = {0,0,1};
	float vx[3] = {0,0,1};
	float vy[3] = {0,0,0};
	float *dev_x, *dev_y;
	float *dev_vx, *dev_vy;

	struct Elem E = {{0,1,2},10,0.4};
	struct Elem *dev_E;

//	cudaMalloc((void **) &dev_Fx, sizeof(float));
//	cudaMalloc((void **) &dev_Fy, sizeof(float));
//	cudaMalloc((void **) &dev_x, sizeof(float));
//	cudaMalloc((void **) &dev_y, sizeof(float));
//	cudaMalloc((void **) &dev_vx, sizeof(float));
//	cudaMalloc((void **) &dev_vy, sizeof(float));
//	cudaMalloc((void **) &dev_E, sizeof(Elem));

//	cudaMemcpy(dev_Fx,Fx,sizeof(float)*3,cudaMemcpyHostToDevice);
//	cudaMemcpy(dev_Fy,Fy,sizeof(float)*3,cudaMemcpyHostToDevice);
//	cudaMemcpy(dev_x,x,sizeof(float)*3,cudaMemcpyHostToDevice);
//	cudaMemcpy(dev_y,y,sizeof(float)*3,cudaMemcpyHostToDevice);
//	cudaMemcpy(dev_vx,vx,sizeof(float)*3,cudaMemcpyHostToDevice);
//	cudaMemcpy(dev_vy,vy,sizeof(float)*3,cudaMemcpyHostToDevice);	
//	cudaMemcpy(dev_E,&E,sizeof(Elem),cudaMemcpyHostToDevice);

//	GenForce<<<1,1>>>(&dev_Fx,&dev_Fy,dev_E,dev_x,dev_y,1,dev_vx,dev_vy);
	GenForce(Fx,Fy,&E,x,y,1,vx,vy);

//	cudaMemcpy(Fx,dev_Fx,sizeof(float)*3,cudaMemcpyDeviceToHost);
//	cudaMemcpy(Fy,dev_Fy,sizeof(float)*3,cudaMemcpyDeviceToHost);

	for(i=0;i<3;i++)
		printf("%f %f\n",Fx[i],Fy[i]);

	return 0;	
}
