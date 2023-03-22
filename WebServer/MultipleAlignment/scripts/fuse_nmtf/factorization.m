function [S,G] = factorization(R,A,k,gamma,max_iter)
% Function for computing block matrix factors, S and G, obtained by using NMTF factorization
% -------------------------------------------------------------------------------------------------------------
% Vladimir Gligorijevic
% Imperial College London
% v.gligorijevic@imperial.ac.uk
% Last updated: 2/12/2014
% --------------------------------------------------------------------------------------------------------------
% Implementaiton based on the paper:
% Wang, F., Li T., Zhang, C., Semi-Supervised Clustering via Matrix Factorization, In SDM, pp. 1-12. 2008
% 
% [Input]:
%     R: <2D Cell array >, r(node types) x r(node types) blocks, relational matrix (e.g., R{i,j} = Rij, 
%     ni(nodes of type i) x nj(nodes of type j))
%     A: <1D Cell array>, r (node types) blocks, adjacency matrix (e.g., A{i} = Ai, ni (nodes) x ni (nodes)) 
%     k: <array>, rank parameters (e.g., [k1, k2,...,kr])
%     gamma: <float>, regularization parameter
%     max_iter: <int>, predefined number of iterations 
%
% [Output]: 
%     S: <2D Cell>, r(node types) x r(node types) blocks, compressed matrix (e.g., S{i,j} = Sij, ki x kj)
%     G: <1D Cell>, r(node types) blocks, cluster indicator matrix (e.g., G{i} = Gi, ni x ki)
% --------------------------------------------------------------------------------------------------------------


% number of data sources (node types)
size_R = size(R);
r = size_R(1);

% computing norm of R matrix
norm_R = 0;
for i=1:r
    for j=i+1:r
        norm_R = norm_R + (norm(R{i,j},'fro'))^2;
    end;
end;

% For of each data source
fprintf('-Initializations of G matrices....\n');
n = [];
for ii=1:r
    % Laplacian matrices
    L_pos{ii} = diag(sum(A{ii},1));
    L_neg{ii} = A{ii}; 
    n(ii) = length(A{ii}); % sizes (number of genes)
    
    % Matrix initialization
    G{ii} = rand(n(ii),k(ii)); 
    fprintf('Initialization of %d matrix finished!\n',ii);
end;
fprintf('-Initialization of G matrices finished!\n\n');

J_old = 0; %initialization
%Iterations 
fprintf('| Iteration | Delta_R | Cost | RSE | Rel_Var_Cost | \n');
for iter=1:max_iter
    
     
    GtG = blkdiag(G{:})'*blkdiag(G{:}) + eps;
    GtG_inv = inv(GtG);
    
    % Update S
    S = GtG_inv*blkdiag(G{:})'*cell2mat(R)*blkdiag(G{:})*GtG_inv;
    S = mat2cell(S,k,k); % block represenation (cell)
    
    % Initialize sum (numerator and denominator)
    for ll=1:r
        Ge{ll} = zeros(n(ll),k(ll));
        Gd{ll} = zeros(n(ll),k(ll));
    end;
    
    % Update G
    for i=1:r
        for j=1:r
            if (i ~= j & (isempty(R{i,j}) == 0 | length(find(R{i,j} ~= 0)) == 0))
                RGSt = R{i,j}*G{j}*S{i,j}';
                RtGS = R{i,j}'*G{i}*S{i,j};
                GtGi = G{i}'*G{i};
                GtGj = G{j}'*G{j};
                SGtGSt = S{i,j}*GtGj*S{i,j}';
                StGtGS = S{i,j}'*GtGi*S{i,j};
                RGSt_pos = (abs(RGSt)+RGSt)/2.0;
                RGSt_neg = (abs(RGSt)-RGSt)/2.0;
                RtGS_pos = (abs(RtGS)+RtGS)/2.0;
                RtGS_neg = (abs(RtGS)-RtGS)/2.0;
                SGtGSt_pos = (abs(SGtGSt)+SGtGSt)/2.0;
                SGtGSt_neg = (abs(SGtGSt)-SGtGSt)/2.0;
                StGtGS_pos = (abs(StGtGS)+StGtGS)/2.0;
                StGtGS_neg = (abs(StGtGS)-StGtGS)/2.0;
                
                
                Ge{i} = Ge{i} + RGSt_pos + G{i}*SGtGSt_neg;
                Gd{i} = Gd{i} + RGSt_neg + G{i}*SGtGSt_pos;
                Ge{j} = Ge{j} + RtGS_pos + G{j}*StGtGS_neg;
                Gd{j} = Gd{j} + RtGS_neg + G{j}*StGtGS_pos;
            end;
        end;
    end;
    
    % Adding constraints and computing new values for Gi
    for t=1:r
        Ge{t} = Ge{t} + gamma*L_neg{t}*G{t};
        Gd{t} = Gd{t} + gamma*L_pos{t}*G{t};
        
        % Updating new values (Output)
        G{t} = G{t}.*(sqrt(Ge{t}./Gd{t}));
    end;

    % Computing the relative square error (RSE) every 10th iteration
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    % (n-1)th iteration 
    if mod(iter+1,10) == 0    
        
        relation_error = 0;
        penalty = 0; 
        for i=1:r
            penalty = penalty + trace(G{i}'*(L_pos{i}-L_neg{i})*G{i});
            for j=i+1:r
                relation_error = relation_error + (norm( R{i,j} - G{i}*S{i,j}*G{j}', 'fro' ))^2;
            end;
        end;
        % objective (cost) function
        J_old = relation_error + penalty;
    
    end;
    
    % nth iteration 
    if mod(iter,10) == 0    
        
        relation_error = 0;
        penalty = 0; 
        for i=1:r
            penalty = penalty + trace(G{i}'*(L_pos{i}-L_neg{i})*G{i});
            for j=i+1:r
                relation_error = relation_error + (norm( R{i,j} - G{i}*S{i,j}*G{j}', 'fro' ))^2;
            end;
        end;
        % objective (cost) function
        J_new = relation_error + penalty;
    
        
        % Errors
        RSE = relation_error/norm_R;
        rel_var = abs(J_new - J_old)/abs(J_old);
        
        % Writing output
        fprintf('%d %0.5e %0.5e %0.5e %0.5e\n', iter, relation_error, J_new, RSE, rel_var);
    
        if (RSE <= 1e-3 | rel_var <= 1e-5) % checking for convergence
            break;
        end;
    
    end;

end; 
