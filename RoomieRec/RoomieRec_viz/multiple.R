
format_multiple <- function(file) {
  
  multiple <- read.csv(file)
  
  for (i in 1:nrow(multiple)) {
    if (multiple[i,4] %in% c("","        google map\n       ","Antioch, Concord, Dublin","COMMUTER BED For student use/ access to Ebay Colleges",
                             "Modesto - Lodi - Stockton","SCCVMED","Tracy","UCB or CSUEB/BART to anywhere","campbell", 
                             "east san jose","mountain view","Oakland","OAKLAND")) {
      multiple[i,4] <- NA
    }else if (multiple[i,4]  == '1675 Hays street') {
      multiple[i,4] <- "danville / san ramon"
    }else if (multiple[i,4]  == "Alameda") {
      multiple[i,4] <- 'alameda'
    }else if (multiple[i,4]  == 'beinica') {
      multiple[i,4] <- "vallejo / benicia"
    }else if (multiple[i,4]  %in% c('Brentwood / Oakley','East Bay - Tracy - Brentwood - Manteca - Stockton')) {
      multiple[i,4] <- "brentwood / oakley"
    }else if (multiple[i,4]  %in% c('Berkeley','Berkeley/Albany')) {
      multiple[i,4] <- 'berkeley'
    }else if (multiple[i,4]  %in% c('Castro Valley','Hayward/Castro Valley')) {
      multiple[i,4] <- 'hayward / castro valley'
    }else if (multiple[i,4]  %in% c('Laurel District','Oak Hills, by BART')) {
      multiple[i,4] <- 'oakland hills / mills'
    }else if (multiple[i,4]  == 'Ivy Hill/Bella Vista neighborhood Oakland') {
      multiple[i,4] <- 'oakland east'
    }else if (multiple[i,4]  %in% c('Martinez','Pleasant Hill','Near Bay Point BART')) {
      multiple[i,4] <- 'concord / pleasant hill / martinez'
    }else if (multiple[i,4]  %in% c('San Leandro','San Leandro - BART STATION','SAN LEANDRO - Near BART',
                                    'San Leandro/ close to your College/Bart','SAN LEANDRO','SAN LEANDRO - BAY FAIR BART',
                                    'San Leandro/ close to your College')) {
      multiple[i,4] <- 'san leandro'
    }else if (multiple[i,4]  == 'Vallejo') {
      multiple[i,4] <- 'vallejo / benicia'
    }else if (multiple[i,4]  == 'WAlnut creek') {
      multiple[i,4] <- 'walnut creek'
    }
  }
  multiple$neighborhood <- factor(multiple$neighborhood, ordered = T)
  levels(multiple$neighborhood)
  
  multiple$room <- 0
  multiple$bath <- 0
  multiple$cat <- 0
  multiple$dog <- 0
  multiple$furnished <- 0
  multiple$smoke <- 0
  multiple$wheelchair <- 0
  multiple$laundry <- 0
  multiple$parking <- 0
  check <- c("'private room'", "'private bath'", "'cats are OK - purrr'", "'dogs are OK - wooof'", "'furnished'",
             "'no smoking'", "'wheelchair accessible'")
  laundry <- c("'w/d in unit'", "'laundry in bldg'", "'laundry on site'")
  parking <- c("'carport'", "'attached garage'", "'detached garage'", "'off-street parking'", "'street parking'",
               "'valet parking'")
  for (i in 1:nrow(multiple)) {
    attributes <- stri_extract_all_regex(multiple[i,7], "'(.*?)'")
    for (j in 1:length(attributes[[1]])) {
      att <- attributes[[1]][j]
      if (att %in% check) {
        index <- match(att, check)
        multiple[i,(10+index)] <- 1
      }else if (att %in% laundry) {
        multiple[i,18] <- 1
      }else if (att %in% parking) {
        multiple[i,19] <- 1
      }
    }
  }
  
  multiple <- aggregate(multiple[, c(11:19)], list(multiple$neighborhood), function(x) round(mean(x,na.rm=T)*100, digits=0))
  multiple <- reshape2::melt(multiple, id.vars = c('Group.1'), variable.name = "attribute", value.name = "percentage")
  levels(multiple$attribute) <- c("private room", "private bath", "cats are OK - puuur", "dogs are OK - wooof", "furnished",
                                "no smoking", "wheelchair accessible", "laundry", "parking")
  return(multiple)
  
}