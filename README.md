# Style Transfer

Objective: Transfer the styles of an an artistic piece to a content image. Our inspiration originates from artists such as Monet, Dali, and Van Gogh. If there were present in our current time, what would their portraits be? What would the skyline appear as to Davinci? Our goal is to transfer their artistic styles to any image that can be taken in present day. 

We scraped artistic pieces from www.wikiart.org/, where we search for the name of the top 100 most influential artists of all time. All the data was saved to a csv before being loaded to the data page in our Flask file. After finding our style transfer inspiration on [colab](https://colab.research.google.com/github/tensorflow/models/blob/master/research/nst_blogpost/4_Neural_Style_Transfer_with_Eager_Execution.ipynb), we transferred the code to python and modified the layers to match our needs. Our final application includes a full functioning site that uses HTML and JS to allow to user to either select an art piece from our library, or upload their own, along with a content image to apply the transfer to. 

When you get the chance, check it out [here!](https://inspiring-depictions.herokuapp.com/)
