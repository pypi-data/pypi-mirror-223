#ifndef ISOOPERATOR_H
#define ISOOPERATOR_H

#include <string>
using std::string;

/* Elastic Propagator (forward or adjoint)

parameters:
    para_fname: parameter file name
    gpu_id: gpu id
    group_size: number of shots
    shot_ids: shot id array
    Lambda: Lambda array
    Mu: Mu array
    Den: Den array
    stf: source time function array
    is_acoustic: acoustic or elastic
        false: elastic
        true: acoustic
    with_adj: adjoint model
        false: forward modeling
        true: adjoint modeling after forward modeling, with the forward modeling
        data as the adjoint source for testing the adjointness of the forward
*/

extern "C" void Propagator(const string para_fname, const int gpu_id,
                           const int group_size, const int *shot_ids,
                           const float *Lambda, const float *Mu,
                           const float *Den, const float *stf,
                           const bool is_acoustic, const bool with_adj);

/* Gradient (misfit or misfit + gradient)

parameters:
    para_fname: parameter file name
    gpu_id: gpu id
    group_size: number of shots
    shot_ids: shot id array
    Lambda: Lambda array
    Mu: Mu array
    Den: Den array
    stf: source time function array
    misfit: misfit value
    grad_Lambda: gradient of Lambda
    grad_Mu: gradient of Mu
    grad_Den: gradient of Den
    grad_Vp: gradient of Vp (for acoustic)
    grad_stf: gradient of stf
    is_acoustic: acoustic or elastic
        false: elastic
        true: acoustic
    with_grad: gradient
        false: only calculate misfit
        true: calculate misfit + gradient
*/

extern "C" void Gradient(const string para_fname, const int gpu_id,
                         const int group_size, const int *shot_ids,
                         const float *Lambda, const float *Mu,
                         const float *Den, const float *stf,
                         float *misfit, float *grad_Lambda,
                         float *grad_Mu, float *grad_Den, float *grad_Vp,
                         float *grad_stf, const bool is_acoustic,
                         const bool with_adj);

#endif