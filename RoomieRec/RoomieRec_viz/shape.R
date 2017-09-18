
format_shape <- function(file) {
  
  map <- read.csv(file)
  map <- unique(map)
  # these are probably weekly/monthly or scams
  map <- map[!(map$price < 200),]
  
  id <- vector("list", nrow(map))
  for (i in 1:nrow(map)) {
    if (map[i,4] %in% c("", "COMMUTER BED For student use access to Ebay Colleges", "Modesto - Lodi - Stockton", "Tracy", "SCCVMED", "UCB or CSUEB/BART to anywhere", "google map")) {
      id[[i]] <- list(NA)
    }else if (map[i,4] %in% c("1675 Hays street")) {
      id[[i]] <- list("SAN RAMON")
    }else if (map[i,4] %in% c("Alameda", "alameda")) {
      id[[i]] <- list("ALAMEDA")
    }else if (map[i,4] %in% c("Antioch, Concord, Dublin")) {
      id[[i]] <- list("ANTIOCH", "CONCORD", "DUBLIN")
    }else if (map[i,4] %in% c("berkeley", "berkeley north / hills", "Berkeley")) {
      id[[i]] <- list("BERKELEY")
    } else if (map[i,4] %in% c("brentwood / oakley", "Brentwood / Oakley")) {
      id[[i]] <- list("BRENTWOOD", "OAKLEY")
    } else if (map[i,4] %in% c("danville / san ramon")) {
      id[[i]] <- list("DANVILLE", "SAN RAMON")
    }else if (map[i,4] %in% c("campbell")) {
      id[[i]] <- list("SAN JOSE")
    }else if (map[i,4] %in% c("East Bay - Tracy - Brentwood - Manteca - Stockton")) {
      id[[i]] <- list("BRENTWOOD")
    }else if (map[i,4] %in% c("emeryville")) {
      id[[i]] <- list("EMERYVILLE")
    }else if (map[i,4] %in% c("fremont / union city / newark")) {
      id[[i]] <- list("FREMONT", "UNION CITY", "NEWARK")
    }else if (map[i,4] %in% c("Hayward/Castro Valley", "hayward / castro valley")) {
      id[[i]] <- list("HAYWARD", "CASTRO VALLEY")
    }else if (map[i,4] %in% c("Ivy Hill/Bella Vista neighborhood Oakland", "Oakland", "Laurel District", "oakland downtown", 
                              "oakland hills / mills", "oakland north / temescal", "oakland rockridge / claremont", "Oak Hills, by BART",
                              "OAKLAND", "oakland east", "oakland lake merritt / grand", "oakland piedmont / montclair", "oakland west")) {
      id[[i]] <- list("OAKLAND")
    }else if (map[i,4] %in% c("Near Bay Point BART")) {
      id[[i]] <- list("CONCORD")
    }else if (map[i,4] %in% c("pittsburg / antioch")) {
      id[[i]] <- list("PITTSBURG", "ANTIOCH")
    }else if (map[i,4] %in% c("richmond / point / annex")) {
      id[[i]] <- list("RICHMOND")
    }else if (map[i,4] %in% c("San Leandro", "San Leandro - BART STATION", "SAN LEANDRO - Near BART", "San Leandro/ close to your College/Bart",
                              "SAN LEANDRO", "SAN LEANDRO - BAY FAIR BART", "San Leandro/ close to your College", "san leandro")) {
      id[[i]] <- list("SAN LEANDRO")
    }else if (map[i,4] %in% c("Vallejo")) {
      id[[i]] <- list("VALLEJO")
    }else if (map[i,4] %in% c("walnut creek", "WAlnut creek")) {
      id[[i]] <- list("WALNUT CREEK")
    }else if (map[i,4] %in% c("albany / el cerrito")) {
      id[[i]] <- list("ALBANY", "EL CERRITO")
    }else if (map[i,4] %in% c("beinica")) {
      id[[i]] <- list("BENICIA")
    }else if (map[i,4] %in% c("Berkeley/Albany")) {
      id[[i]] <- list("BERKELEY", "ALBANY")
    }else if (map[i,4] %in% c("Castro Valley")) {
      id[[i]] <- list("CASTRO VALLEY")
    }else if (map[i,4] %in% c("concord / pleasant hill / martinez")) {
      id[[i]] <- list("CONCORD", "PLEASANT HILL", "MARTINEZ")
    }else if (map[i,4] %in% c("dublin / pleasanton / livermore")) {
      id[[i]] <- list("DUBLIN", "PLEASANTON", "LIVERMORE")
    }else if (map[i,4] %in% c("east san jose")) {
      id[[i]] <- list("SAN JOSE")
    }else if (map[i,4] %in% c("fairfield / vacaville")) {
      id[[i]] <- list("FAIRFIELD")
    }else if (map[i,4] %in% c("hercules, pinole, san pablo, el sob")) {
      id[[i]] <- list("HERCULES", "PINOLE", "SAN PABLO", "EL SOBRANTE")
    }else if (map[i,4] %in% c("lafayette / orinda / moraga")) {
      id[[i]] <- list("LAFAYETTE", "ORINDA", "MORAGA")
    }else if (map[i,4] %in% c("Martinez")) {
      id[[i]] <- list("MARTINEZ")
    }else if (map[i,4] %in% c("mountain view")) {
      id[[i]] <- list("MOUNTAIN VIEW")
    }else if (map[i,4] %in% c("Pleasant Hill")) {
      id[[i]] <- list("PLEASANT HILL")
    }else if (map[i,4] %in% c("vallejo / benicia")) {
      id[[i]] <- list("VALLEJO", "BENICIA")
    }else {
      id[[i]] <- list(NA)
    }
  }
  map$shape <- NA
  i <- 1
  while (i < 1823) {
    map[i,11] <- id[[i]][1]
    if (length(id[[i]]) > 1) {
      for (j in 2:length(id[[i]])) {
        new <-data.frame(c(map[i,1:10], shape=id[[i]][j]))
        map <- rbind(map, new)
      }
    }
    i <- i + 1
  }
  map <- map[-which(is.na(map$shape)),]
  map$size <- as.numeric(as.character(map$size))
  df <- aggregate(map[, c(3,6)], list(map$shape), function(x) mean(x,na.rm=T))
  names(df) <- c("CITY", "avg_price", "avg_size")
  
  map <- readOGR(".", "bay_area_cities")
  map_wgs84 <- spTransform(map, CRS("+proj=longlat +datum=WGS84"))
  area <- map_wgs84
  
  df.polygon2 <- area 
  df.polygon2@data$rec <- 1:nrow(df.polygon2@data)
  tmp <- left_join(df.polygon2@data, df, by="CITY") %>% 
    arrange(rec)
  df.polygon2@data <- tmp
  df.polygon2 <- df.polygon2[!is.na(df.polygon2@data$avg_price), ]
  df.polygon2 <- df.polygon2[!is.na(df.polygon2@data$avg_size), ]
  df.polygon2@data$CITY <- c("Alameda", "Albany", "Antioch", "Benicia", "Berkeley", "Brentwood", "Castro Valley", "Concord", "Danville", 
                             "Dublin", "El Cerrito", "El Sobrante", "Emeryville", "Fairfield", "Fremont", "Hayward", "Hercules", 
                             "Lafayette", "Livermore", "Martinez", "Moraga", "Newark", "Oakland", "Oakley", "Orinda", "Pinole", 
                             "Pittsburg", "Pleasant Hill", "Pleasanton", "Richmond", "San Jose", "San Leandro", "San Pablo", "San Ramon",
                             "Union City", "Vallejo", "Walnut Creek", "Alameda", "Alameda", "Alameda")
  return (df.polygon2)
}
