% The MAIN function for calling performing NMTF step
%-------------------------------------------------------------------------
% Based on the article: "Fuse: Multiple Network Alignment via Data Fusion"
% Authors: Vladimir Gligorijevic, Noel Malod-Dognin and Natasa Przulj
% Imperial College London
%-------------------------------------------------------------------------
% Vladimir Gligorijevic
% Imperial College London
% Email: v.gligorijevic@imperial.ac.uk
% Last updated: 2/12/2014
%-------------------------------------------------------------------------
%
% [Input]: 
%
% 1) adj_list: <string cell array>, file names of networks given in the edgelist 
%    format: node_i node_j w_ij 
% 2) rel_file: <string>, name of the file containing BLAST sequence 
%    similarities between all proteins in all the species (e.g. 
%    'sequence-similarity.lst'). Format of the file: node_i node_j  -log(eval_ij)
% 3) k: <int array>, list of rank parameters to start the (e.g., [80,90,80,70,50])
% 4) iter_num: <int>, number of NMTF iterations (e.g. 1000)
% 5) gamma: <float>, regularization parameter (e.g. 0.01)
%
%% [Output]: 
%
% 6) sim_file: <string>, name of the file with exported, significant protein-protein 
% similarities (e.g. 'output_similarities.txt') 

function run_nmtf(adj_list, rel_file, k, iter_num, gamma, sim_file)

fprintf('---STEP 1:\n');
fprintf('---------------------------------------------------------\n');
fprintf('---Reading all networks and creating block matrices....\n\n');
[R,A,label_list] = block_matrices(adj_list, rel_file);
fprintf('---Finished!\n\n');

fprintf('---STEP 2:\n');
fprintf('---------------------------------------------------------\n');
fprintf('---Factorization of matrices using NMTF...\n\n');
[S,G] = factorization(R, A, k, gamma, iter_num);
fprintf('---Finished!\n\n');

fprintf('---STEP 3:\n');
fprintf('---------------------------------------------------------\n');
fprintf('---Exporting significant associaitons from reconstructed matrix...\n');
top_export(G, S, label_list, sim_file, 5.0);
fprintf('---Finished!\n\n');
