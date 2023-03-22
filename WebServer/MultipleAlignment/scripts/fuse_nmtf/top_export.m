% Reconstructed relation matrices -> only top 5% of protin associations 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function top_export(G, S, label_list, sim_file, top_p)

fprintf('\n---Creating reconstructed relation matrix (only upper blocks)...\n');
for i=1:length(label_list)
    sizes(i) = length(label_list{i});
end;
tol = 1e-5; % minimum association score (evrything lower than this is considered zero)

% unique list of all proteins (converting string to num)
unique_list = str2double([label_list{:}]);

r = length(sizes); % number of networks
Rapprox = mat2cell(zeros(sum(sizes),sum(sizes)),sizes,sizes);
for i=1:r
    for j=i+1:r
        Rapprox{i,j} = G{i}*S{i,j}*G{j}';
        Rapprox{i,j} = Rapprox{i,j}.*(Rapprox{i,j}>tol);
        fprintf('--Relation matrix between network %d and %d finished.\n',i,j);
    end;
end;
fprintf('---Finished\n\n');

% Constructing matrix from 2D cell
Rapprox = cell2mat(Rapprox);

% Checking
sz = size(Rapprox);
if sz(1) ~= sum(sizes)
    error('Relation matrix dimension doesnt agree!');
end;

% Exporting relations
fid = fopen(sim_file,'w');

fprintf(fid,'Gene1 | Gene2 | Association_score\n');
for i=1:sz(1)
    dist = sort(nonzeros([Rapprox(i,:) Rapprox(:,i)']),'descend');
    if length(dist) > 0
        threshold = dist(max(1, round((top_p/100.0)*length(dist))));
        ind = [find(Rapprox(i,:) >= threshold) find(Rapprox(:,i) > threshold)'];
        for j=1:length(ind)
            if (i < ind(j))
                fprintf(fid,'%d %d %f\n',unique_list(i),unique_list(ind(j)),Rapprox(i,ind(j)));
            end;
        end;
    end;
    if mod(i,1000) == 0
        fprintf('Finished %d proteins out of %d.\n',i,sz(1));
    end;
end;
fclose(fid);

fprintf('--Writing significant protein associatons finished!');
