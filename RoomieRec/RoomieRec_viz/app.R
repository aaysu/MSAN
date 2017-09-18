library(shiny)
library(leaflet)
library(ggplot2)
library(ggvis)
library(rgdal)
library(dplyr)
library(reshape2)
library(stringi)
source("shape.R")
source("map.R")
source("multiple.R")
source("scatter.R")

options(warn=-1)

colors = c("#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9")

# format data for each plot
df.polygon2 <- format_shape("cleaned_all_craigslist.csv")
map <- format_map("cleaned_all_craigslist.csv")
multiple <- format_multiple("cleaned_all_craigslist.csv")
scatter <- format_scatter("cleaned_all_craigslist.csv")


ui <- fluidPage(
  titlePanel(title = 'Visualizing Craigslist Room Listings in the East Bay'),
  mainPanel(
    tabsetPanel(
      tabPanel("Dot Map", 
               fluidRow(
                 column(4, sliderInput("map_price", label = h5("Price Range ($)"), min = 0, max = 5300, value = c(0, 5300), step = 100, sep = "", ticks = F)),
                 column(4, sliderInput("map_size", label = h5("Size Range (sqft)"), min = 0, max = 4000, value = c(0, 4000), step = 100, sep = "", ticks = F)),
                 column(4, selectInput("map_att", label = h5("Attributes"), multiple = T,
                                        choices = list("private room" = 11, "private bath" = 12, "cats are OK - puuur" = 13, "dogs are OK - wooof" = 14, 
                                                       "furnished" = 15, "no smoking" = 16, "wheelchair accessible" = 17, "laundry" = 18, "parking" = 19),
                                        selected = NULL))
               ),
               leafletOutput("map", height = 600, width = 900)),
      tabPanel("Choropleth Map", leafletOutput("shape", height = 700, width = 900)),
      tabPanel("Small Multiples",
               selectizeInput("multiple_neigh", label = h5("Neighborhoods"), multiple=T, options = list(maxItems = 5), 
                           choices = list("alameda" = "alameda", "albany / el cerrito" = "albany / el cerrito",
                                          "berkeley" = "berkeley", "berkeley north / hills" = "berkeley north / hills",
                                          "brentwood / oakley" = "brentwood / oakley", "concord / pleasant hill / martinez" = "concord / pleasant hill / martinez", 
                                          "danville / san ramon" = "danville / san ramon", "dublin / pleasanton / livermore" = "dublin / pleasanton / livermore",
                                          "emeryville" = "emeryville", "fairfield / vacaville" = "fairfield / vacaville", 
                                          "fremont / union city / newark" = "fremont / union city / newark", "hayward / castro valley" = "hayward / castro valley",
                                          "hercules, pinole, san pablo, el sob" = "hercules, pinole, san pablo, el sob",
                                          "lafayette / orinda / moraga" = "lafayette / orinda / moraga", "oakland downtown" = "oakland downtown",
                                          "oakland east" = "oakland east", "oakland hills / mills" = "oakland hills / mills",
                                          "oakland lake merritt / grand" = "oakland lake merritt / grand", "oakland north / temescal" = "oakland north / temescal",
                                          "oakland piedmont / montclair" = "oakland piedmont / montclair", "oakland rockridge / claremont" = "oakland rockridge / claremont",
                                          "oakland west" = "oakland west", "pittsburg / antioch" = "pittsburg / antioch",
                                          "richmond / point / annex" = "richmond / point / annex", "san leandro" = "san leandro",
                                          "vallejo / benicia" = "vallejo / benicia", "walnut creek" = "walnut creek"),
                           selected = c("alameda","albany / el cerrito","berkeley","berkeley north / hills","brentwood / oakley")),
               plotOutput("multiple")),
      tabPanel("Scatter Plot",
               fluidRow(
                 column(5, selectInput("region", label = NULL,
                                       choices = list("Region 1" = "Region 1", "Region 2" = "Region 2", "Region 3" = "Region 3",
                                                      "Region 4" = "Region 4", "Region 5" = "Region 5"),
                                       selected = "Region 1")),
                 column(5, selectInput("neighborhood", label = NULL,
                                       choices = list("All Neighborhoods" = 1, "alameda" = "alameda", "albany / el cerrito" = "albany / el cerrito",
                                                      "berkeley" = "berkeley", "berkeley north / hills" = "berkeley north / hills",
                                                      "brentwood / oakley" = "brentwood / oakley", "concord / pleasant hill / martinez" = "concord / pleasant hill / martinez", 
                                                      "danville / san ramon" = "danville / san ramon", "dublin / pleasanton / livermore" = "dublin / pleasanton / livermore",
                                                      "emeryville" = "emeryville", "fairfield / vacaville" = "fairfield / vacaville", 
                                                      "fremont / union city / newark" = "fremont / union city / newark", "hayward / castro valley" = "hayward / castro valley",
                                                      "hercules, pinole, san pablo, el sob" = "hercules, pinole, san pablo, el sob",
                                                      "lafayette / orinda / moraga" = "lafayette / orinda / moraga", "oakland downtown" = "oakland downtown",
                                                      "oakland east" = "oakland east", "oakland hills / mills" = "oakland hills / mills",
                                                      "oakland lake merritt / grand" = "oakland lake merritt / grand", "oakland north / temescal" = "oakland north / temescal",
                                                      "oakland piedmont / montclair" = "oakland piedmont / montclair", "oakland rockridge / claremont" = "oakland rockridge / claremont",
                                                      "oakland west" = "oakland west", "pittsburg / antioch" = "pittsburg / antioch",
                                                      "richmond / point / annex" = "richmond / point / annex", "san leandro" = "san leandro",
                                                      "vallejo / benicia" = "vallejo / benicia", "walnut creek" = "walnut creek"), 
                                       selected = 1))
               ),
               ggvisOutput("scatter"))
    )
  )
)

server <- function(input, output, session) {
  
  filteredData <- reactive({
    max_price <- input$map_price[2]
    min_price <- input$map_price[1]
    new_map <- map[(map$price <= max_price) & (map$price >= min_price),]
    max_size <- input$map_size[2]
    min_size <- input$map_size[1]
    new_map <- new_map[(new_map$size <= max_size) & (new_map$size >= min_size),]
    attributes <- input$map_att
    for (index in attributes) {
      new_map <- new_map[new_map[as.numeric(index)] == 1, ]
    }
    new_map
  })
  
  output$map <- renderLeaflet({
    pal_map <- colorBin(palette = "Reds", domain = map$price, bins = c(0,500,700,900,1100,1500,5300))
    bounds <- c(-122.1, 37.7, -122.5, 38)
    leaflet(map) %>%
      addProviderTiles("Hydda.Full") %>%
      addLegend(pal = pal_map, values = map$price, title = "Price", labFormat=labelFormat(prefix='$', between = " - $", big.mark=""), opacity = 0.8) %>%
      fitBounds(bounds[1], bounds[2], bounds[3], bounds[4])
  })
  
  observe({
    pal_map <- colorBin(palette = "Reds", domain = map$price, bins = c(0,500,700,900,1100,1500,5300))
    leafletProxy("map", data = filteredData()) %>%
      clearMarkers() %>%
      addCircleMarkers(~longitude, ~ latitude, 
                 color = "black",
                 fillColor = ~pal_map(price), 
                 weight = 1,
                 fillOpacity = 0.8, 
                 radius = 10,
                 #highlightOptions = highlightOptions(color = "white", weight = 1, bringToFront = TRUE, fillOpacity = 1),
                 popup = ~paste("<style> div.leaflet-popup-content-wrapper { opacity: 0.8; } </style>", "<div id='background'></div>", 
                                '<b>', title, '</b>', '<br>', popup, sep = ''))
  })
  
  output$shape <- renderLeaflet({
    pal_shape <- colorBin(palette = "Reds", domain = df.polygon2@data$avg_price, pretty=T)
    map <- leaflet() %>%
      addProviderTiles("Hydda.Full") %>%
      addPolygons(data = df.polygon2,
                  color = "black",
                  fillColor = ~pal_shape(avg_price),
                  weight = 1,
                  fillOpacity = 0.8,
                  highlightOptions = highlightOptions(color = "white", weight = 1, bringToFront = TRUE, fillOpacity = 1),
                  popup = ~paste("<style> div.leaflet-popup-content-wrapper { opacity: 0.8; } </style>", "<div id='background'></div>",
                                 '<b>', CITY, '</b>', '<br>', "Average Price: $", round(avg_price, digits=0), "<br>", "Average Size: ",
                                 round(avg_size, digits=0), " sqft", sep = ''),popupOptions = ) %>%
      addLegend(pal = pal_shape, values = df.polygon2@data$avg_price, title = "Average Price", labFormat=labelFormat(prefix='$', between = " - $", big.mark=""), opacity = 0.8)
  })
  
  scatter$id <- 1:nrow(scatter)
  all_values <- function(x) {
    if(is.null(x)) return(NULL)
    row <- scatter[scatter$id == x$id, ]
    paste('<b>', row$title, '</b>', '<br>', 'Neighborhood: ', row$neighborhood, '<br>', "Price: $", row$price, "<br>", "Size: ", row$size, " sqft", sep = '')
  }
  
  observe({
    keep <- scatter[scatter$region == input$region,]
    neighborhoods <- unique(sort(keep$neighborhood))
    updateSelectInput(session, "neighborhood", label = NULL,
                      choices = list("All Region Neighborhoods" = 1, neighborhoods = neighborhoods),
                        selected = 1)
  })
  
  filteredData_scatt <- reactive({
    keep <- scatter[scatter$region == input$region,]
    keep$neighborhood <- factor(keep$neighborhood, ordered = T)
    keep
  })
  
  vis <- reactive({
    keep <- filteredData_scatt()
    num <- length(levels(keep$neighborhood))
    if (input$neighborhood != 1) {
      keep <- keep[keep$neighborhood == input$neighborhood,]
    }
    ggvis() %>%
      layer_points(data=keep, ~size, ~price, size := 300, key := ~id, fill = ~neighborhood, 
                   fillOpacity := 0.7, fillOpacity.hover := 1, stroke := "black", stroke.hover := "white")  %>%
      add_axis("x", title = "Size (sqft)") %>%
      add_axis("y", title = "Price ($)", title_offset = 50) %>%
      add_tooltip(all_values, "hover") %>%
      add_legend("fill", title="Neighborhood") %>%
      scale_numeric("x", domain = c(min(scatter$size),max(scatter$size))) %>%
      scale_numeric("y", domain = c(min(scatter$price),max(scatter$price))) %>%
      scale_ordinal("fill", range=colors[1:num]) %>%
      set_options(width = 925, height = 625)
  })
  vis %>% bind_shiny("scatter")
  
  filteredData_mult <- reactive({
    multiple[(multiple$Group.1 %in% input$multiple_neigh), ]
  })
  
  output$multiple <- renderPlot({
    if (nrow(filteredData_mult()) > 0) {
      g2 <- ggplot(data=filteredData_mult(), aes(x=Group.1, y=percentage)) +
        geom_bar(aes(fill=Group.1), colour="black", stat="identity") +
        facet_wrap(~attribute, labeller = label_value) +
        coord_flip() +
        ylab("\nListings in Neighborhood with Attribute (%)") +
        xlab("Neighborhood\n") +
        labs(colour = "legend title") +
        labs(fill = "Neighborhood") +
        theme(legend.background = element_rect(size=0.25, linetype="solid", colour ="black"),
              legend.text = element_text(size = 12),
              legend.title = element_text(size = 14),
              axis.title = element_text(size = 18),
              axis.text = element_text(size = 12),
              panel.background = element_blank(),
              panel.grid.major = element_line(colour = "grey", size = 0.25),
              panel.grid.minor = element_line(colour = "grey", size = 0.25),
              panel.border = element_rect(colour="black", fill = NA),
              strip.text = element_text(size = 12),
              strip.background = element_rect(colour = "black"),
              plot.margin = unit(c(1,1,1,1), "cm")) +
        scale_fill_manual(values=c("#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3"))
      g2
    }
  },height = 600, width = 900)
  
}

shinyApp(ui = ui, server = server)


