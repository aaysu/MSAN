
format_scatter <- function(file) {
  
  scatter <- read.csv(file)
  scatter <- scatter[-881,]
  scatter <- scatter[-86,]
  scatter <- scatter[scatter$size != '',]
  scatter <- scatter[!is.na(scatter$price),]
  
  for (i in 1:nrow(scatter)) {
    if (scatter[i,4]  == 'Berkeley/Albany') {
      scatter[i,4] <- 'berkeley'
    }else if (scatter[i,4]  == 'Castro Valley') {
      scatter[i,4] <- 'hayward / castro valley'
    }else if (scatter[i,4]  == 'Laurel District') {
      scatter[i,4] <- 'oakland hills / mills'
    }else if (scatter[i,4]  == 'Oak Hills, by BART') {
      scatter[i,4] <- 'oakland hills / mills'
    }else if (scatter[i,4]  == 'Vallejo') {
      scatter[i,4] <- 'vallejo / benicia'
    }
  }
  scatter$neighborhood <- factor(scatter$neighborhood, ordered = T)
  
  scatter$region <- NA
  for (i in 1:nrow(scatter)) {
    if (scatter[i,4]  %in% c("oakland downtown",                   
                           "oakland east",
                           "oakland hills / mills", 
                           "oakland lake merritt / grand",      
                           "oakland north / temescal",
                           "oakland piedmont / montclair",   
                           "oakland rockridge / claremont",      
                           "oakland west",
                           "alameda")) {
      scatter[i,11] <- 'Region 1'
    }else if (scatter[i,4]  %in% c("albany / el cerrito",
                                   "berkeley",                           
                                   "berkeley north / hills",
                                   "emeryville")) {
      scatter[i,11] <- 'Region 2'
    }else if (scatter[i,4]  %in% c("richmond / point / annex",
                                   "hercules, pinole, san pablo, el sob",
                                   "fairfield / vacaville",
                                   "vallejo / benicia")) {
      scatter[i,11] <- 'Region 3'
    }else if (scatter[i,4]  %in% c("concord / pleasant hill / martinez",
                                   "lafayette / orinda / moraga",
                                   "pittsburg / antioch",
                                   "walnut creek",
                                   "brentwood / oakley")) {
      scatter[i,11] <- 'Region 4'
    }else if (scatter[i,4] %in% c("danville / san ramon",
                                  "dublin / pleasanton / livermore",
                                  "hayward / castro valley",
                                  "san leandro",
                                  "fremont / union city / newark")) {
      scatter[i,11] <- 'Region 5'
    }
  }

  scatter$size <- as.numeric(as.character(scatter$size))
  scatter <- scatter[!is.na(scatter$size),]
  return (scatter)
}


