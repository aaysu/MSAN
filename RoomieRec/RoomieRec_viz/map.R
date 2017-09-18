
format_map <- function(file) {

  map <- read.csv(file)
  map$movein <- lapply(map$movein, function(x) gsub(" 00:00:00",'',x))
  map <- map[!is.na(map$longitude),]
  map <- map[!is.na(map$price),]
  map$size <- as.numeric(as.character(map$size))
  
  map$room <- 0
  map$bath <- 0
  map$cat <- 0
  map$dog <- 0
  map$furnished <- 0
  map$smoke <- 0
  map$wheelchair <- 0
  map$laundry <- 0
  map$parking <- 0
  check <- c("'private room'", "'private bath'", "'cats are OK - purrr'", "'dogs are OK - wooof'", "'furnished'",
             "'no smoking'", "'wheelchair accessible'")
  laundry <- c("'w/d in unit'", "'laundry in bldg'", "'laundry on site'")
  parking <- c("'carport'", "'attached garage'", "'detached garage'", "'off-street parking'", "'street parking'",
               "'valet parking'")
  for (i in 1:nrow(map)) {
    attributes <- stri_extract_all_regex(map[i,7], "'(.*?)'")
    for (j in 1:length(attributes[[1]])) {
      att <- attributes[[1]][j]
      if (att %in% check) {
        index <- match(att, check)
        map[i,(10+index)] <- 1
      }else if (att %in% laundry) {
        map[i,18] <- 1
      }else if (att %in% parking) {
        map[i,19] <- 1
      }
    }
  }
  
  create_popup <- function(price, movein, size){
    if (!is.na(price)) {
      price <-  c("Price : $", price, "<br>")
    }else {
      price <-  c('', '', '')
    }
    if (!is.na(size)) {
      size <- c("Size: ", size, ' sqft', "<br>")
    }else {
      size <-  c('', '', '', '')
    }
    if (movein != '') {
      movein <- c("Move-in date: ", movein, "<br>")
    }else {
      movein <-  c('', '', '')
    }
    return (paste(price[1], price[2], price[3], size[1], size[2], size[3], size[4], movein[1], movein[2], movein[3], sep = ''))
  }
  popup <- vector()
  for (i in 1:nrow(map)) {
    popup <- c(popup, create_popup(map[i,3], map[i,5], map[i,6]))
  }
  map$popup <- popup
  
  map$size <- as.numeric(as.character(map$size))
  return (map)
}

