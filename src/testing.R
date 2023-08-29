kmnri <-
    function(risklimits, pold, pnew, ftime, censvar, weight = NULL) {
        n <- length(censvar)
        risklimits <- sort(unique(c(0, setdiff(risklimits, 1))))
        print(c(risklimits, 1 + 1e-05))
        ngroup <- length(risklimits)
        print(ngroup)
        if (is.null(weight)) {
            weight <- rep(1, n)
        }
        events <- match(sort(unique(ftime[censvar == 1])), ftime) -1
        print(sort(events))
        print(length(events))

        results <- .C("kmnriw",
            numeric(2),
            numeric(2),
            numeric(1),
            as.double(c(risklimits, 1 + 1e-05)),
            as.double(pold),
            as.double(pnew),
            as.double(ftime),
            as.double(weight),
            as.integer(events),
            as.integer(length(events)),
            as.integer(censvar),
            as.integer(n),
            as.integer(ngroup),
            integer(ngroup^2),
            PACKAGE = "validstats"
        )
        return(list(
            casesup = (results[[1]])[2], casesdown = (results[[2]])[2],
            noncasesup = (results[[1]])[1], noncasesdown = (results[[2]])[1]
        ))
    }

data <- read.csv("data/data.csv")
preds <- c("base", "big")
event_time <- "time"
event <- "status"
r_boot_nri <- 50
parallel <- NULL
cpus <- 1
Time <- time_span <- 600
pold <- data$pred_base
pnew <- data$pred_big
ftime <- data$time
censvar <- data$status
risklimits <- c(0.9)

v <- which(ftime > Time)
if (length(v) > 0) {
    censvar[v] <- 0
    ftime[v] <- Time
}

data <- na.omit(data.frame(
    "pold" = pold, "pnew" = pnew,
    "ftime" = ftime, "censvar" = censvar
))

kmnri(
    risklimits = risklimits,
    pold = data$pold,
    pnew = data$pnew,
    ftime = data$ftime,
    censvar = data$censvar,
    weight = NULL
)
