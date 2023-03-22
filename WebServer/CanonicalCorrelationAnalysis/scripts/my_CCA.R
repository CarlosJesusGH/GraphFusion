args<-commandArgs(TRUE)

geigen <- function(Amat, Bmat, Cmat)
{
  #  solve the generalized eigenanalysis problem
  #
  #    max {tr L'AM / sqrt[tr L'BL tr M'CM] w.r.t. L and M
  #
  #  Arguments:
  #  AMAT ... p by q matrix
  #  BMAT ... order p symmetric positive definite matrix
  #  CMAT ... order q symmetric positive definite matrix
  #  Returns:
  #  VALUES ... vector of length s = min(p,q) of eigenvalues
  #  LMAT   ... p by s matrix L
  #  MMAT   ... q by s matrix M

  Bdim <- dim(Bmat)
  Cdim <- dim(Cmat)
  if (Bdim[1] != Bdim[2]) stop('BMAT is not square')
  if (Cdim[1] != Cdim[2]) stop('CMAT is not square')
  p <- Bdim[1]
  q <- Cdim[1]
  s <- min(c(p,q))
  if (max(abs(Bmat - t(Bmat)))/max(abs(Bmat)) > 1e-10) stop(
    'BMAT not symmetric.')
  if (max(abs(Cmat - t(Cmat)))/max(abs(Cmat)) > 1e-10) stop(
    'CMAT not symmetric.')
  Bmat  <- (Bmat + t(Bmat))/2
  Cmat  <- (Cmat + t(Cmat))/2
  Bfac  <- chol(Bmat)
  Cfac  <- chol(Cmat)
  Bfacinv <- solve(Bfac)
  Cfacinv <- solve(Cfac)
  Dmat <- t(Bfacinv) %*% Amat %*% Cfacinv
  if (p >= q) {
    result <- svd(Dmat)
    values <- result$d
    Lmat <- Bfacinv %*% result$u
    Mmat <- Cfacinv %*% result$v
  } else {
    result <- svd(t(Dmat))
    values <- result$d
    Lmat <- Bfacinv %*% result$v
    Mmat <- Cfacinv %*% result$u
  }
  geigenlist <- list (values, Lmat, Mmat)
  names(geigenlist) <- c('values', 'Lmat', 'Mmat')
  return(geigenlist)
}


my_CCA <- function(X_name, Y_name, prefix)
{
  X <- read.csv(file=X_name,head=FALSE,sep="\t")
  Y <- read.csv(file=Y_name,head=FALSE,sep="\t")
  XY <- cbind(X,Y)
  dimX <- dim(X)[2]
  dimY <- dim(Y)[2]
  
  all_COV <- cov(XY)
  COV_XX <- all_COV[1:dimX, 1:dimX]
  COV_YY <- all_COV[(dimX+1):(dimX+dimY), (dimX+1):(dimX+dimY)]
  COV_XY <- all_COV[1:dimX, (dimX+1):(dimX+dimY)]
  cca <- tryCatch(
    {
        #Try processing covariance matrix directly
	geigen(COV_XY, COV_XX, COV_YY)
    },
    error=function(cond) {
        #If matrices are not regular/invertible, we then regularise them
        print('Regularizing data')
	geigen(COV_XY, COV_XX + diag(1., max(1, ncol(X))), COV_YY + diag(1., max(1, ncol(Y))))
    }
  )
  write.csv(cca$Lmat, paste(prefix, '_X-weights.csv', sep='_'))
  write.csv(cca$Mmat, paste(prefix, '_Y-weights.csv', sep='_'))
  write.csv(cca$values, paste(prefix, '_XY-chi.csv', sep='_'))
}

my_CCA(args[1], args[2], args[3])
