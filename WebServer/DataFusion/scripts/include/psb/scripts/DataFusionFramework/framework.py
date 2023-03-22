import pandas as pd
import numpy as np

def datafusionframework_triPMF(R12, R23, L2, L3, G1, G2, G3, H12, H23, maxIter=1000, itStopChecking=10, verbose=False, eps=5, epsilon=1e-5, gamma_2=1, gamma_3=1):
    
    """
      Adaptation of the data fusion framework from Gligorijevic et. al. 2016 based on the tri-PMF (Wang et. al. 2008)
      
      R12 = G1.H12.G2^T
      R23 = G2.H23.G3^T
      Contrained with G2^T.L2.G2 and G3^T.L3.G3
      
      
    Parameters
    ----------
    
    R12 : numpy array
        Contains the relational matrix between the entity 1 and entity 2 
    R23 : numpy array
        Contains the relational matrix between the entity 2 and entity 3 
    L2 : numpy array
        Contains the laplacian matrix with the raltion among entity 2 
    L3 : numpy array
        Contains the laplacian matrix with the raltion among entity 3 
    G1 : numpy array
        Contains the matrix factor corresponding to the entity 1
    G2 : numpy array
        Contains the matrix factor corresponding to the entity 2
    G3 : numpy array
        Contains the matrix factor corresponding to the entity 3
    H12 : numpy array
        Contains the matrix factor corresponding to the middle factor in the decomposition of R12
    H23 : numpy array
        Contains the matrix factor corresponding to the middle factor in the decomposition of R23
    maxIter : float 
        Indicates the maximum number of iteration after which the iterative process will stop. By default 1000
    itStopChecking : float 
        Indicates the number of iteration between the check of the stop criterion. By default 10
    verbose : boolean
        Indicates whether information of the progress should be printed. By default False
    eps : int 
        Indicates the exponent of the tolerance in the stop criterion. By defaut 5
    epsilon : float
        Indicates the epsilon to be add to the denominators to avoid dividing by 0. By degaul 1e-5
    gamma_2 : float betwen 0 and 1
        Indicates the weigth of the contribution of the constrain associated with the entity 2. By default 1
    gamma_3 : float betwen 0 and 1
        Indicates the weight of the contribution of the constrain associated with the entity 3. By default 1
    
    Return
    ------
    The factors obtained in the decomposition and a list with the error of each iteration
    """

    
    errHistory = [1]
    it = 0
    stop = False
    
    while (it < maxIter) and not stop:
        

            
        #--------------------------------------------------------
        #                     
        # F update H12 and H23
        #
        #--------------------------------------------------------                        
          
        # Update rule for H12, contribution from R12 = G1.H12.G2^T
        # Closed formula: H12 <- (G1T.G1)^-1 G1T.R12.G2 (G2T.G2)^-1
        G1TG1 = np.matmul(G1.T, G1)
        G2TG2 = np.matmul(G2.T, G2)
        G1TG1_inv = np.linalg.inv(G1TG1)                 
        G2TG2_inv = np.linalg.inv(G2TG2)

        H12 = np.matmul(G1TG1_inv, np.matmul(G1.T, np.matmul(R12, np.matmul(G2, G2TG2_inv)))) + epsilon                     
        
                         
        # Update rule for H23, contribution from R23 = G2.H23.G3^T
        # Closed formula: H12 <- (G2T.G2)^-1 G2T.R23.G3 (G3T.G3)^-1
        G3TG3 = np.matmul(G3.T, G3)
        G3TG3_inv = np.linalg.inv(G3TG3)                 
        
        H23 = np.matmul(G2TG2_inv, np.matmul(G2.T, np.matmul(R23, np.matmul(G3, G3TG3_inv)))) + epsilon  
        
        
        #--------------------------------------------------------
        #                     
        # First, update G2, which depends on two decompositions
        #
        #--------------------------------------------------------      
        
        
        #Update rule for G2, contribution from R12 = G1.H12.G2^T
        # G2 <- G2 ([R12T.G1.H12]_pos + G2.[H12^T.G1^T.G1.H12]_neg / [R12.G1.H12]_neg + G2.[H12^T.G1^T.G1.H12]_pos )
        R12T_G1_H12 = np.matmul(R12.T, np.matmul(G1, H12))
        R12T_G1_H12_pos = (np.absolute(R12T_G1_H12) + R12T_G1_H12)/2.0
        R12T_G1_H12_neg = (np.absolute(R12T_G1_H12) - R12T_G1_H12)/2.0    
                             
        H12T_G1TG1_H12 = np.matmul(H12.T, np.matmul(G1.T, np.matmul(G1, H12)))
        G2_H12T_G1TG1_H12_pos = np.matmul(G2, ((np.absolute(H12T_G1TG1_H12) + H12T_G1TG1_H12)/2.0))
        G2_H12T_G1TG1_H12_neg = np.matmul(G2, ((np.absolute(H12T_G1TG1_H12) - H12T_G1TG1_H12)/2.0))                     
                                                      
        G2Num1 = R12T_G1_H12_pos + G2_H12T_G1TG1_H12_neg
        G2Denom1 = R12T_G1_H12_neg + G2_H12T_G1TG1_H12_pos

                             
        #Update rule for G2, contribution from R23 = G2.H23.G3^T
        # G2 <- G2 ([R23.G3.H23T]_pos + G2.[H23.G3^T.G3.H23^T]_neg / [R23.G3.H23T]_neg + G2.[H23.G3^T.G3.H23^T]_pos )
        R23_G3_H23T = np.matmul(R23, np.matmul(G3, H23.T))
        R23_G3_H23T_pos = (np.absolute(R23_G3_H23T) + R23_G3_H23T)/2.0
        R23_G3_H23T_neg = (np.absolute(R23_G3_H23T) - R23_G3_H23T)/2.0    
                             
        H23_G3TG3_H23T = np.matmul(H23, np.matmul(G3.T, np.matmul(G3, H23.T)))
        G2_H23_G3TG3_H23T_pos = np.matmul(G2, ((np.absolute(H23_G3TG3_H23T) + H23_G3TG3_H23T)/2.0))
        G2_H23_G3TG3_H23T_neg = np.matmul(G2, ((np.absolute(H23_G3TG3_H23T) - H23_G3TG3_H23T)/2.0))
                                   
        G2Num2 = R23_G3_H23T_pos + G2_H23_G3TG3_H23T_neg
        G2Denom2 = R23_G3_H23T_neg + G2_H23_G3TG3_H23T_pos

        # Contrain on G2, contribution from G2T.L2.G2
        G2Const_pos = np.matmul(((np.absolute(L2) + L2)/2.0), G2) 
        G2Const_neg = np.matmul(((np.absolute(L2) - L2)/2.0), G2)    
       
        #Check that we are note dividing by zero  
        G2update = np.sqrt(np.divide(G2Num1 + G2Num2 + gamma_2*G2Const_neg + epsilon , G2Denom1 + G2Denom2 + gamma_2*G2Const_pos + epsilon))
        G2 = np.multiply(G2, G2update)  + epsilon 
           
                
         
        #--------------------------------------------------------
        #                     
        # Now update G1 and G3  
        #
        #--------------------------------------------------------    

        # Update rule for G1, contribution from R12 = G1.H12.G2^T
        # G1 <- G1 ([R12.G2.H12^T]_pos + G1.[H12.G2^T.G2.H12^T]_neg / [R12.G2.H12^T]_neg + G1.[H12.G2^T.G2.H12^T]_pos )
        R12_G2_H12T = np.matmul(R12, np.matmul(G2, H12.T))
        R12_G2_H12T_pos = (np.absolute(R12_G2_H12T) + R12_G2_H12T)/2.0
        R12_G2_H12T_neg = (np.absolute(R12_G2_H12T) - R12_G2_H12T)/2.0    
                             
        H12_G2TG2_H12T = np.matmul(H12, np.matmul(G2.T, np.matmul(G2, H12.T)))
        G1_H12_G2TG2_H12T_pos = np.matmul(G1, ((np.absolute(H12_G2TG2_H12T) + H12_G2TG2_H12T)/2.0))
        G1_H12_G2TG2_H12T_neg = np.matmul(G1, ((np.absolute(H12_G2TG2_H12T) - H12_G2TG2_H12T)/2.0))

                                   
        G1Num = R12_G2_H12T_pos + G1_H12_G2TG2_H12T_neg
        G1Denom = R12_G2_H12T_neg + G1_H12_G2TG2_H12T_pos
        
        #Check that we are note dividing by zero  
        G1update = np.sqrt(np.divide(G1Num + epsilon , G1Denom + epsilon))
        G1 = np.multiply(G1, G1update) + epsilon
        
                             
                             
                                    
        # Update rule for G3, contribution from R23 = G2.H23.G3^T
        # G3 <- G3 ([R23T.G2.H23]_pos + G3.[H23^T.G2^T.G2.H23^T]_neg / [R23T.G2.H23]_neg + G3.[H23^T.G2^T.G2.H23^T]_pos )
        R23T_G2_H23 = np.matmul(R23.T, np.matmul(G2, H23))
        R23T_G2_H23_pos = (np.absolute(R23T_G2_H23) + R23T_G2_H23)/2.0
        R23T_G2_H23_neg = (np.absolute(R23T_G2_H23) - R23T_G2_H23)/2.0    
                             
        H23T_G2TG2_H23T = np.matmul(H23.T, np.matmul(G2.T, np.matmul(G2, H23)))
        G3_H23T_G2TG2_H23T_pos = np.matmul(G3, ((np.absolute(H23T_G2TG2_H23T) + H23T_G2TG2_H23T)/2.0))
        G3_H23T_G2TG2_H23T_neg = np.matmul(G3, ((np.absolute(H23T_G2TG2_H23T) - H23T_G2TG2_H23T)/2.0))
                                   
        G3Num = R23T_G2_H23_pos + G3_H23T_G2TG2_H23T_neg
        G3Denom = R23T_G2_H23_neg + G3_H23T_G2TG2_H23T_pos
                             
        # Contrain on G2, contribution from G2T.L2.G2
        G3Const_pos = np.matmul(((np.absolute(L3) + L3)/2.0), G3)
        G3Const_neg = np.matmul(((np.absolute(L3) - L3)/2.0), G3)     
                            
        
        #Check that we are note dividing by zero  
        G3update = np.sqrt(np.divide(G3Num + gamma_3*G3Const_neg + epsilon , G3Denom + gamma_3*G3Const_pos + epsilon))
        G3 = np.multiply(G3, G3update) + epsilon
                      
        

        #Using numpy norm funtion
        Err1 = R12 - np.matmul(G1,  np.matmul(H12, G2.T))
        norm_err1 = np.linalg.norm(Err1, ord='fro')


        Err2 = R23 - np.matmul(G2,  np.matmul(H23, G3.T))
        norm_err2 = np.linalg.norm(Err2, ord='fro')


        Err3 = np.trace(np.matmul(G2.T, np.matmul(L2, G2)))
        Err4 = np.trace(np.matmul(G3.T, np.matmul(L3, G3)))

        E = norm_err1**2 + norm_err2**2 + gamma_2*Err3 + gamma_3*Err4
        errHistory.append(E)


        errStop = np.abs(E - errHistory[-2])/np.abs(errHistory[-2])           
        stop = errStop  - 10**(-eps) < 0

        if verbose and(it % itStopChecking == 0):
            print("  -->Error Relative {} : {}".format(it, errStop))
            
        # update iteration count and stop criteria
        it += 1

    print("  -->Error Relative {} : {}".format(it, errStop))
    
    factors = H12, H23, G1, G2, G3
    err = errHistory[1:]
    return factors, err