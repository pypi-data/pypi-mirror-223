import numpy as np


from imagex.utils import split_model


# Abstract class
class AbstractProblem(object):
    ''' Problem class
    '''

    def __init__(self):
        pass

    # Helper method
    def die(self, cls):
        """ Helper function to exit when class in not defined"""
        raise NotImplementedError("Method "+cls+" has not been overritten")

    def apply_gradient(self):
        self.die("apply_gradient")

    def save_model(self):
        self.die("save_model")


class ElasticProblem(AbstractProblem):
    ''' Problem class
    '''

    def __init__(self, propagator):
        ''' Initialize the problem class
        ''' 

        self.propagator = propagator

        # set the default scaling factors to rescale the gradient and cost
        self.scale_factor_vp = 30.0
        self.scale_factor_vs = 18.0
        self.scale_factor_rho = 6.0


    def apply_gradient(self, model, grad_vp_mask, grad_vs_mask, grad_rho_mask, 
                       stf = None, ngpu=1, first_iter=False):
        
        # check the model parameters exist
        vp, vs, rho = split_model(model, self.propagator.nx, self.propagator.nz)

        # check the vp/vs ratio and clip it if necessary
        ratio_min = 0.0
        ratio_max = 1/np.sqrt(2) - 0.01
        ratio = np.clip(vs/vp, ratio_min, ratio_max)
        vp[ratio != 0] = vs[ratio != 0] / ratio[ratio != 0]

        # computation of the cost and gradient
        fcost, grad_vp, grad_vs, grad_rho, grad_stf = self.propagator.apply_gradient(vp, vs, rho, ngpu=ngpu)


        # apply the gradient mask   
        grad_vp *= grad_vp_mask
        grad_vs *= grad_vs_mask
        grad_rho *= grad_rho_mask

        # set proper scaling factors
        if first_iter:
            if np.max(np.abs(grad_vp)) > 0:
                self.scale_factor_vp = self.scale_factor_vp / np.max(np.abs(grad_vp))

            if np.max(np.abs(grad_vs)) > 0:
                self.scale_factor_vs = self.scale_factor_vs / np.max(np.abs(grad_vs))
           
            if np.max(np.abs(grad_rho)) > 0:
                self.scale_factor_rho = self.scale_factor_rho / np.max(np.abs(grad_rho))
            
    
        # rescale the gradient and cost
        grad_vp *= self.scale_factor_vp
        grad_vs *= self.scale_factor_vs
        grad_rho *= self.scale_factor_rho
        fcost *= self.scale_factor_vp

        # merge the gradient
        grad = np.concatenate((grad_vp.flatten(), grad_vs.flatten(), grad_rho.flatten()))
        grad_preco = np.copy(grad)


        # TODO: add the gradient of the source time function
        return fcost, grad, grad_preco


    def save_model(self, model, grad, file_name):
        ''' Save the model parameters and gradient
        '''

        vp, vs, rho = split_model(model, self.propagator.nx, self.propagator.nz)
        grad_vp, grad_vs, grad_rho = split_model(grad, self.propagator.nx, self.propagator.nz)

        # save the model parameters as dictionary
        model_dict = {'vp': vp, 'vs': vs, 'rho': rho, 'grad_vp': grad_vp, 
                      'grad_vs': grad_vs, 'grad_rho': grad_rho}
        
        # save the model parameters
        np.savez(file_name, **model_dict)

        # save the model parameters as npy files
        np.save(file_name.replace("_result", "_vp"), vp)
        np.save(file_name.replace("_result", "_vs"), vs)
        np.save(file_name.replace("_result", "_rho"), rho)


class SimuElasticProblem(AbstractProblem):
    ''' Simultaneous problem class
    '''

    def __init__(self, Problem1, Problem2, weight1, weight2):
        ''' Initialize the problem class
        ''' 

        self.Problem1 = Problem1
        self.Problem2 = Problem2
        self.weight1 = weight1
        self.weight2 = weight2

        # set the default scaling factors to rescale the gradient and cost
        self.Problem1.scale_factor_vp = 30.0
        self.Problem1.scale_factor_vs = 18.0
        self.Problem1.scale_factor_rho = 6.0

        self.Problem2.scale_factor_vp = 30.0
        self.Problem2.scale_factor_vs = 18.0
        self.Problem2.scale_factor_rho = 6.0


    def apply_gradient(self, model, grad_vp_mask, grad_vs_mask, grad_rho_mask, 
                        stf = None, ngpu=1, first_iter=False):

        # split the model
        model1 = model[:int(len(model)/2)]
        model2 = model[int(len(model)/2):]

        # compute the cost function and gradient for the first problem
        fcost1, grad1, grad_preco1 = self.Problem1.apply_gradient(model1, grad_vp_mask, 
                            grad_vs_mask, grad_rho_mask, stf, ngpu, first_iter)

        # compute the cost function and gradient for the second problem
        fcost2, grad2, grad_preco2 = self.Problem2.apply_gradient(model2, grad_vp_mask, 
                            grad_vs_mask, grad_rho_mask, stf, ngpu, first_iter)

        # add the two cost functions and gradients
        fcost = self.weight1 * fcost1 + self.weight2 * fcost2

        grad = np.concatenate((self.weight1 *grad1, self.weight2 * grad2))
        grad_preco = np.concatenate((self.weight1 *grad_preco1, self.weight2 * grad_preco2))

        # TODO: add the regularization term

        return fcost, grad, grad_preco
    
    def save_model(self, model, grad, file_name):
        ''' Save the model parameters and gradient
        '''

        bl_file_name = file_name.replace("_result", "_bl_result")
        ml_file_name = file_name.replace("_result", "_ml_result")

        self.Problem1.save_model(model[:int(len(model)/2)], grad[:int(len(model)/2)], bl_file_name)
        self.Problem2.save_model(model[int(len(model)/2):], grad[int(len(model)/2):], ml_file_name)