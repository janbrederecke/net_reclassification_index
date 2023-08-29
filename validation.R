
data <- read.csv("data/data.csv")
data$pred_big2 <- data$pred_big * 1.1
preds <- c("base", "big", "big2")
event_time <- "time"
event <- "status"
r_boot_nri <- 50
parallel <- NULL
cpus <- 1
risklimits_nri_score <- c(0.9)
time_span <- 600

# Net reclassification 

library(boot)
# Categorical NRI function wrapper (using boot package) 
categ_nri_boot <- function(risklimits, pold, pnew, ftime, censvar, Time, Nboot, 
                           parallel = "no", ncpus = 1){
  v <- which(ftime > Time)
  if (length(v) > 0) {
    censvar[v] <- 0
    ftime[v] <- Time 
  }
  
  Data <- na.omit(data.frame("pold" = pold, "pnew" = pnew,
                             "ftime" = ftime, "censvar" = censvar))
  
  kmnri_boot <- function(data, indices) {
    require(validstats)
    data <- data[indices, ]
    a <- kmnri(risklimits = risklimits, 
               pold = data$pold, 
               pnew = data$pnew, 
               ftime = data$ftime, 
               censvar = data$censvar, weight = NULL) 
    print(a)
    nri.ev <- a[["casesup"]] - a[["casesdown"]]
    nri.nev <- a[["noncasesdown"]] - a[["noncasesup"]]
    nri <- nri.ev + nri.nev
    return(c("nri.ev" = nri.ev, "nri.nev" = nri.nev, "nri" = nri))
  }
  
  results <- boot(data = Data, statistic = kmnri_boot,
                  R = Nboot, parallel = parallel, ncpus = cpus)
  
#print(results$t0)

  SE <- apply(results$t, 2, sd, na.rm = TRUE)
  nri.ev  <- results$t0[1]
  nri.nev <- results$t0[2]
  nri     <- results$t0[3]
  names(nri) <- names(nri.ev) <- names(nri.nev) <- NULL
  
  out <- c("nri" = nri, "nri.SE" = SE[3], 
           "nri.p" = 2 * pnorm(-abs(nri)/SE[3]),
           "nri.ev" = nri.ev, "nri.ev.SE" = SE[1], 
           "nri.ev.p" = 2 * pnorm(-abs(nri.ev)/SE[1]),
           "nri.nev" = nri.nev, "nri.nev.SE" = SE[2], 
           "nri.nev.p" = 2 * pnorm(-abs(nri.nev)/SE[2]), "N" = nrow(Data), 
           "Nevent" = sum(Data$censvar))  
}

# NRI on available cases dataset 
wrapper <- function(pred) categ_nri_boot(risklimits = risklimits_nri_score, 
                                         pold = data[, paste0("pred_", preds[1])], 
                                         pnew = data[, paste0("pred_", pred)], 
                                         ftime = data[[event_time]], 
                                         censvar = data[[event]], 
                                         Time = time_span, Nboot = r_boot_nri, 
                                         parallel = parallel, ncpus = cpus)

nri_matrix_ac <- do.call("rbind", lapply(preds[-1], wrapper))


# Processing NRI_MATRIX_AC 
process_nri <- function(x){
  
  qqq <- qnorm(0.975)
  
  out <- cbind(nri = x[, "nri"], 
               nri.left = x[, "nri"] - qqq * x[, "nri.SE"] ,
               nri.right = x[, "nri"] + qqq * x[, "nri.SE"],
               
               nri.ev = x[, "nri.ev"], 
               nri.ev.left = x[, "nri.ev"] - qqq * x[, "nri.ev.SE"] ,
               nri.ev.right = x[, "nri.ev"] + qqq * x[, "nri.ev.SE"],
               
               nri.nev = x[, "nri.nev"], 
               nri.nev.left = x[, "nri.nev"] - qqq * x[, "nri.nev.SE"] ,
               nri.nev.right = x[, "nri.nev"] + qqq * x[, "nri.nev.SE"],
               
               N = x[, "N"], Nevent = x[, "Nevent"]
  )
  
}

rows <- rownames(nri_matrix_ac)


nri_matrix_ac <- process_nri(nri_matrix_ac)
rownames(nri_matrix_ac) <- rows

nri_matrix_ac
