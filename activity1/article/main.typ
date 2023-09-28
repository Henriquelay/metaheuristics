#let author = "Henrique Coutinho Layber"
#let institution = "Federal University of Espírito Santo"
#let title = "A survey on Guided Local Search (GLS)"
#set document(title: title, author: author)
// This has no visible output, but embeds metadata into the PDF!

#set text(
  font: "New Computer Modern",
)
#set par(justify: true)
#set page(header: locate(loc => {
  if counter(page).at(loc).first() > 1 [
    #title
    #h(1fr)
    #institution
  ]
}))

#align(center, text(17pt)[
  * #title *
])


#grid(
  columns: (1fr),
  align(center)[
    #author \
    #institution \
    #link("mailto:henrique.layber@edu.ufes.br") \
    `2018103824`
  ]
)

#show heading: it => [
//   #set align(center)
  #block(smallcaps(it.body))
]


= Introduction
// Explain in general what will be presented. Algorithm characteristics, main applications.

#outline()

= History

= State of the art

= Definition

= Description

= Applying on Timetable problem (TTP)

= Conclusion
#cite("harry")

= References

#bibliography("works.yml")
