import json 
import os
import logging

import azure.functions as func
import azure.cosmos as cosmos
import azure.cosmos.exceptions as exceptions
import math
import random
import config

recipes = [
	{
		"macros": [{"name": "fat", "amount": "9", "unit": "g"}, {"name": "carbs", "amount": "34", "unit": "g"}, {"name": "protein", "amount": "16", "unit": "g"}],
		"difficulty": "medium",
		"steps": [{"content": "Add a spoonful of oil into a pot and heat it", "key": "1", "name": "Step" }, {"content": "In the meantime, dice up an onion and cook it in the pot until it caramelized", "key": "2", "name": "Step" }, {"content": " Put the ground meat into the pot and cook for about 20 minutes. Add salt, pepper, and chili powder to the meat as it\'s cooking to taste", "key": "3", "name": "Step" }, {"content": "After about 20 minutes, put in the mushrooms, corn, beans and tomato sauce and cook for another 5 minutes.", "key": "4", "name": "Step"}],
		"time_to_make":  {"amount": "30", "unit": "min"},
		"ingredients":[{"name": "ground beef or pork", "category": "meat", "quantity": "0.5", "unit": "kg"}, {"name": "baked beans", "category": "vegetables", "quantity": "2", "unit": "cans"}, {"name": "corn", "category": "vegetables", "quantity": "1", "unit": "can"}, {"name": "mushrooms", "category": "vegetables", "quantity": "1", "unit": "can"}, {"name": "onion", "category": "vegetables", "quantity": "1", "unit": "-"}, {"name": "salt", "category": "condiments", "quantity": "to taste", "unit": "-"}, {"name": "pepper", "category": "condiments", "quantity": "to taste", "unit": "-"}, {"name": "chili powder", "category": "condiments", "quantity": "to taste", "unit": "-"}, {"name": "oil", "category": "condiments", "quantity": "1", "unit": "tablespoon"}, {"name": "tomato sauce", "category": "condiments", "quantity": "1", "unit": "can"}],
		"name": "Mexican Chili Beans",
		"image": "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.greatgrubdelicioustreats.com%2Fwp-content%2Fuploads%2F2015%2F12%2FIMG_7040.jpg&f=1&nofb=1&ipt=f95285eb68371d5eda205d2313c277867d32518c30bbb7472541e6bb27628148&ipo=images",
		"price": { "amount": "5", "unit": "GBP" }
	},
	{
		"macros": [{"name": "fat", "amount": "39", "unit": "g"}, {"name": "carbs", "amount": "40", "unit": "g"}, {"name": "protein", "amount": "25", "unit": "g"}],
		"difficulty": "easy",
		"steps": [{"content": "Bring a large pot of lightly salted water to a boil. Add penne and cook, stirring occasionally, until penne start to get tender, about 8 minutes. Drain and reserve 1/4 cup pasta water.", "key": "1", "name": "Step" }, {"content": "Preheat the oven to 375 degrees F (190 degrees C). ", "key": "2", "name": "Step" }, {"content": " Meanwhile, cook Italian sausage in a heavy skillet over medium-high heat until brown and crumbly, about 5 minutes. Transfer to a paper towel lined plate. ", "key": "3", "name": "Step" }, {"content": "Melt butter in a skillet over medium heat. Sauté minced garlic and red pepper flakes until garlic is fragrant, 30 to 45 seconds. Sprinkle flour over mixture and stir to combine, making sure there are no lumps", "key": "4", "name": "Step"}, {"content": "Pour in milk, cream, and reserved pasta water. Mix mozzarella, provolone, Fontina, and Parmesan cheeses in a bowl and stir in about 4/5th of the cheese mixture. Stir to combine. Add penne, cooked Italian sausage, and tomato sauce to the cheese sauce. Mix to combine and pour into an 8x8 inch casserole dish. Sprinkle with remaining cheese mixture.", "key": "5", "name": "Step"}, {"content": "Bake in the preheated oven until cheese is melted and lightly browned, about 25 minutes.", "key": "6", "name": "Step"}],
		"time_to_make":  {"amount": "45", "unit": "min"},
		"ingredients":[{"name": "penne pasta", "category": "pasta", "quantity": "8", "unit": "ounces"}, {"name": "sausage", "category": "meat", "quantity": "10", "unit": "ounces"}, {"name": "butter", "category": "condiments", "quantity": "1.5", "unit": "tablespoon"}, {"name": "minced garlic", "category": "vegetables", "quantity": "2", "unit": "cloves"}, {"name": "red paprika powder", "category": "condiments", "quantity": "1", "unit": "pinch"}, {"name": "flour", "category": "flour", "quantity": "1", "unit": "tablespoon"}, {"name": "milk", "category": "dairy", "quantity": "1", "unit": "cup"}, {"name": "whipping cream", "category": "dairy", "quantity": "0.5", "unit": "cup"}, {"name": "mozzarella", "category": "cheese", "quantity": "1.25", "unit": "ounces"}, {"name": "provolone", "category": "cheese", "quantity": "1.25", "unit": "ounces"}, {"name": "fontina", "category": "cheese", "quantity": "1.25", "unit": "ounces"}, {"name": "parmesan", "category": "cheese", "quantity": "1.25", "unit": "ounces"}, {"name": "tomato sauce", "category": "sauce", "quantity": "0.25", "unit": "cup"}],
		"name": "Italian Mac And Cheese",
		"image": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwhiskitrealgud.com%2Fwp-content%2Fuploads%2F2018%2F11%2FItalian-Mac-and-Cheese-1.jpg&f=1&nofb=1&ipt=17dc5c48bf690cdff476ce8fe343d183055d292c3b0a53c68d75659d46609e60&ipo=images",
		"price": { "amount": "5", "unit": "GBP" }
	},
	{
		"macros": [{"name": "fat", "amount": "11", "unit": "g"}, {"name": "carbs", "amount": "22", "unit": "g"}, {"name": "protein", "amount": "31", "unit": "g"}],
		"difficulty": "easy",
		"steps": [{"content": "Season chicken breasts on both sides with salt and pepper. Place flour, beaten egg, and panko crumbs into separate shallow dishes. Coat chicken breasts in flour, shaking off any excess; dip into egg, and then press into panko crumbs until well coated on both sides", "key": "1", "name": "Step" }, {"content": "Heat oil in a large skillet over medium-high heat. Place chicken in the hot oil, and fry until golden brown, 3 or 4 minutes per side. Transfer to a paper towel-lined plate to drain.", "key": "2", "name": "Step" }],
		"time_to_make":  {"amount": "25", "unit": "min"},
		"ingredients":[{"name": "skinless, boneless chicken breast halves", "category": "meat", "quantity": "4", "unit": "ounces"}, {"name": "salt", "category": "condiments", "quantity": "to taste", "unit": "-"}, {"name": "pepper", "category": "condiments", "quantity": "to taste", "unit": "-"}, {"name": "flour", "category": "flour", "quantity": "2", "unit": "tablespoon"}, {"name": "egg", "category": "egg", "quantity": "1", "unit": "-"}, {"name": "bread crumbs", "category": "bread", "quantity": "1", "unit": "cup"}, {"name": "oil", "category": "oil", "quantity": "1", "unit": "cup"}],
		"name": "Chicken Katsu",
		"image": "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fangsarap.net%2Fwp-content%2Fuploads%2F2014%2F03%2Fchicken-katsu-wide.jpg&f=1&nofb=1&ipt=bed1a18c34e5bb42617d97f152538aa2da561490288a65e8acd4c331a34abe03&ipo=images",
		"price": { "amount": "5", "unit": "GBP" }
	},
	{
		"macros": [{"name": "fat", "amount": "41", "unit": "g"}, {"name": "carbs", "amount": "48", "unit": "g"}, {"name": "protein", "amount": "29", "unit": "g"}],
		"difficulty": "easy",
		"steps": [{"content": "Saute ground beef in a large skillet over medium heat until browned and crumbly; 5 to 10 minutes.", "key": "1", "name": "Step" }, {"content": "At the same time, fill a large pot with lightly salted water and bring to a rapid boil. Cook egg noodles at a boil until tender yet firm to the bite, 7 to 9 minutes. Drain and set aside. ", "key": "2", "name": "Step" }, {"content": "Drain and discard any fat from the cooked beef. Stir condensed soup and garlic powder into the beef. Simmer for 10 minutes, stirring occasionally.", "key": "3", "name": "Step" }, {"content": "Remove beef from the heat. Add egg noodles and stir to combine. Stir in sour cream and season with salt and pepper.", "key": "4", "name": "Step"}],
		"time_to_make":  {"amount": "20", "unit": "min"},
		"ingredients":[{"name": "egg noodles", "category": "pasta", "quantity": "1", "unit": "package"}, {"name": "salt", "category": "condiments", "quantity": "to taste", "unit": "-"}, {"name": "pepper", "category": "condiments", "quantity": "to taste", "unit": "-"}, {"name": "ground beef", "category": "meat", "quantity": "1", "unit": "pound"}, {"name": "condensed cream of mushroom soup", "category": "sauce", "quantity": "1", "unit": "can"}, {"name": "garlic powder", "category": "condiments", "quantity": "1", "unit": "tablespoon"}, {"name": "sour cream", "category": "condiments", "quantity": "0.5", "unit": "cup"}], 
		"name": "Beef Stroganoff",
		"image": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.platingsandpairings.com%2Fwp-content%2Fuploads%2F2020%2F12%2Finstant-pot-beef-stroganoff-10-1365x2048.jpg&f=1&nofb=1&ipt=054cb22552feafca3297eb1fc864f82b38d12caec2b907bf8b57489f10c1c96f&ipo=images",
		"price": { "amount": "5", "unit": "GBP" }
	},
	{
		"macros": [{"name": "fat", "amount": "4.6", "unit": "g"}, {"name":"protein", "amount": "2.8", "unit": "g"}, {"name": "fiber", "amount": "0.6", "unit": "g"}],
		"difficulty": "easy",
		"steps": [{"content": "If making two small bowls, divide the green onions evenly between two bowls and add 1/4 teaspoon sugar, 1/4 teaspoon chicken bouillon powder, 1 teaspoon sesame oil, and 1 or 2 teaspoons soy sauce to each bowl (depending on preference and the saltiness of the stock used). Add everything to a big bowl if making 1 serving. each bowl. ", "key": "1", "name": "Step" }, {"content": "Bring a pot of water to a boil. At the same time bring the chicken stock to a boil and add 1 cup to each bowl. Stir to dissolve the sugar and chicken bouillon powder. ", "key": "2", "name": "Step" }, {"content": "If adding bok choy or another vegetable blanch them in the boiling water until just cooked through, between 30 seconds to 1 minute, until just cooked through. Distribute the bok choy evenly between the bowls (or if you would like to lay them on top for looks, set them aside and place them on after the noodles are added). ", "key": "3", "name": "Step" }, {"content": "Boil the noodles according to the instructions on the package, try to get them al dente so they don\'t overcook in the broth, usually 1 minute less than indicated on the package.", "key": "4", "name": "Step"}, {"content": "Drain the noodles and rinse briefly under cold water to stop the cooking. Add half to each bowl.", "key": "5", "name": "Step"}, {"content": "Taste and add more sesame oil or soy sauce if needed. Top with other ingredients if using.", "key": "6", "name": "Step"}],
		"time_to_make":  {"amount": "8", "unit": "min"},
		"ingredients":[{"name": "green onion", "category": "vegetable", "quantity": "1", "unit": "piece"}, {"name": "sugar", "category": "condiments", "quantity": "0.5", "unit": "teaspoon"}, {"name": "chicken bouillon powder", "category": "condiments", "quantity": "0.5", "unit": "teaspoon"}, {"name": "sesame oil", "category": "condiments", "quantity": "2", "unit": "teaspoon"}, {"name": "soy sauce", "category": "condiments", "quantity": "2", "unit": "teaspoons"}, {"name": "chicken stock", "category": "condiments", "quantity": "2", "unit": "cups"}, {"name": "thin wheat noodles", "category": "pasta", "quantity": "110", "unit": "gramms"}, {"name": "egg", "category": "egg", "quantity": "1", "unit": "piece"}],
		"name": "Soy Sauce Noodles",
		"image": "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fomnivorescookbook.com%2Fwp-content%2Fuploads%2F2015%2F11%2F1511_Easy-Soy-Sauce-Noodles_002.jpg&f=1&nofb=1&ipt=817fcd69aebf737a560e34a89b89b87b4a3e722b08c19be33d06279561489d16&ipo=images",
		"price": { "amount": "5", "unit": "GBP" }
	},
	{
		"macros": [{"name": "Fat", "amount": "10.9", "unit":"g"}, {"name": "Protein", "amount": "26.4", "unit": "g"}, {"name": "Fiber", "amount": "15.7", "unit": "g"}, {"name": "Sugar", "amount": "20.5", "unit": "g"}],
		"difficulty": "easy",
		"steps": [{"content": "Combine all the sauce ingredients in a small bowl. Stir well and set aside. ", "key": "1", "name": "Step" }, {"content": "Bring a pot of water to a boil. Cook the lo mein noodles according to the instructions on the packaging. Rinse with cool water to stop the cooking and set them aside.", "key": "2", "name": "Step" }, {"content": "Heat the oil in a large nonstick skillet over medium-high heat until hot. Add the garlic, ginger, and green onion and saute until fragrant, about 1 minute.  ", "key": "3", "name": "Step" }, {"content": "Turn the heat to high and add the carrots, snow peas, and baby bok choy. Stir fry until the vegetables begin to soften, 1 to 2 minutes. ", "key": "4", "name": "Step"}, {"content": "Add the cooked lo mein and toss with a pair of tongs to distribute the vegetables. Pour the sauce onto the noodles. Cook, tossing continuously, until the liquid is fully absorbed and the noodles are fully coated.", "key": "5", "name": "Step"}, {"content": "Serve hot as a main dish or side dish.", "key": "6", "name": "Step"}],
		"time_to_make":  {"amount": "20", "unit": "min"},
		"ingredients": [{"name": "lo mein noodles", "category": "pasta", "quantity": "225", "unit": "g"}, {"name": "peanut oil", "category": "condiments", "quantity": "0.5", "unit": "tablespoons"}, {"name": "garlic", "category": "vegetables", "quantity": "1", "unit": "cloves"}, {"name": "ginger", "category": "vegetables", "quantity": "2.5", "unit": "cm"}, {"name": "green onions", "category": "vegetables", "quantity": "1.5", "unit": "-"}, {"name": "snow peas", "category": "vegetables", "quantity": "0.5", "unit": "cup"}, {"name": "sliced carrot", "category": "vegetables", "quantity": "0.4", "unit": "cup"}, {"name": "baby bok choy", "category": "vegetables", "quantity": "2", "unit":"heads"}, {"name": "soy sauce", "category": "condiments", "quantity": "0.5", "unit": "tablespoon"}, {"name": "dark soy sauce", "category": "condiments", "quantity": "2", "unit": "teaspoons"}, {"name": "sugar", "category": "condiments", "quantity": "1", "unit": "teaspoons"}, {"name": "sesame oil", "category": "condiments", "quantity": "0.25", "unit": "teaspoons"}],
		"name": "Vegetable Lo Mein",
		"image": "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fvalentinascorner.com%2Fwp-content%2Fuploads%2F2020%2F01%2FVegetable-Lo-Mein-1.jpg&f=1&nofb=1&ipt=614310106882a45ef1edbe65a17fb3f1077ee4171c6cef6b09cd5eb9a3ebce37&ipo=images",
		"price": { "amount": "5", "unit": "GBP" }
	},
	{
		"macros":[{"name": "Protein","amount": "27","unit": "g"},{"name": "Fat","amount": "7","unit": "g"},{"name": "Carbs","amount": "18","unit": "g"}],
		"difficulty": "easy",
		"steps": [{"content": "Whisk together the hoisin sauce, sesame oil, garlic, ginger, vinegar, and Asian chile paste in a bowl.", "key": 1, "name": "Step 1" },{"content": "Season the beef with salt and pepper.", "key": 2, "name": "Step 2" },{"content": " Heat a non-stick skillet over high heat. Once hot, spray with cooking spray and add the beef. Cook for 3-4 minutes until done to your liking.", "key": 3, "name": "Step 3" },{"content": "Remove the beef and set aside. Add more cooking spray and add the scallions, cabbage, and sauce. Cook for about 5 minutes until the cabbage is cooked.", "key": 4, "name": "Step 4" },{"content": "Turn off the heat and stir in the beef. Top with cilantro.", "key": 5, "name": "Step 5" }],
		"time_to_make": {"amount": "15","unit": "min"},
		"ingredients":[{"name": "hoisin sauce","category": "condiments","quantity": "20","unit": "ml"},{"name": "sesame oil","category": "condiments","quantity": "3","unit": "ml"},{"name": "garlic clove","category": "vegetable","quantity": "0.25","unit": "-"},{"name": "ginger root","category": "vegetable","quantity": "1","unit": "g"},{"name": "rice vinegar","category": "conidments","quantity": "2.5","unit": "ml"},{"name": "asian chile paste","category": "condiments","quantity": "1.5","unit": "ml"},{"name": "lean sirloin steak, cut into strips","category": "meat","quantity": "120","unit": "g"},{"name": "cabbage slaw mix","category": "vegetable","quantity": "100","unit": "g"},{"name": "green onions","category": "vegetable","quantity": "1.5","unit": "-"},{"name": "cilantro","category": "vegetable","quantity": "1","unit": "g"}],
		"name":"Moo Shu Beef Stir Fry",
		"image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBYVFRgVFRYYGBgZGBgYGBgaGBgYGBoYGBgZGRgVGBgcIS4lHB4tHxgYJjgmKy8xNTU2GiQ7QDszPy40NTEBDAwMEA8QHxISHjQrJCs0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NjQ0NDQ0PTQ0NP/AABEIAKgBLAMBIgACEQEDEQH/xAAbAAACAwEBAQAAAAAAAAAAAAADBAECBQYAB//EAD4QAAIBAgQDBgUCBQMBCQAAAAECAAMRBBIhMQVBUQYiYXGBkRMyQqGxwdEUUmLh8CNyghUHFjNTkqKywvH/xAAZAQADAQEBAAAAAAAAAAAAAAAAAQIDBAX/xAAqEQACAgICAQMDBAMBAAAAAAAAAQIRAyESMUEEE1EicYEyYZGhI7HxFP/aAAwDAQACEQMRAD8A7HDJGUWTQTSeBsDJoqyyLCyMMhaHFMxBZRTLkazwUwqrGkFg3ewkNX0vC1KV5kcVr5O6DJnLgrKjHk6IxmNJ0vFke8SwxLMSZqJSnnTm5OzrjFRCUXMYepbaRRpiK4/EZO9yETdKwq2ZPaHiQpZS2msLw/jCOoIInNceU4px/KJp8K4AABvM5NL7lpfJ1C4kOtr3hMNTIF4nhOH5PKatNRaXBN9kypdFb3EvhgQdJUDkI1RS06MMW5WY5JJKhnNK3lZ607zmCq0sJRZcQEVc6RGoSY7VGkUy2iZSITSGdLiDhl2iQMEDaeeSRKONIxkkEjSHpKbayMNtGIJEtg54y9pFoxAnEE0YIlGWAAIMpDlZVhEMzXGsvGWpyloDsWw4vK1MO97WitRyDpynQYdrqD4SVvQdAsNRyiMLCZZ4JKJKlJW0YCSjJAAFR7AmcZxPEXZjOuxyHIbTjsRS0IO85PVyqkdOBLbPcOrgreatOtcWnOYDuXUnnpNrDnpOL9zoNBGsJzHafEE5UzWuZ1WGoM2+kxePcLvURjsJV6FaspwzBAKNJuYemQNp7B0gABHVWc8JpyHKQNWuNZa9oB2JNhGKWHJ3ndCEpGUpJEURreaFNZ6lRtCEgTrhHiqOeUrZ7KJ74co1cctZT456gTSyBnJaQWHWJ1a4tuTFHxcYjTeoOsA+ITqJlVcQWFtovkidi5I1jik6zx4gnWZHw57JCmLkjUPEU6ypxydZmGnBsgHP7w67FzNleIoOcZp8QQ7Ee85spppBshgna0HI65cUp6yRXXrONNRhsTPfx1QfUYw5HaZgdiJVpxw4u43sYanx8je8LKs6mUImLS7QJ9U0aPEUcd1hCx2EMCTDMbxZom6KQiyXmxg/kEzkWaOG+W0S7B9DSmXEErS4MokMNYN5ZGk1BAAF4ri+HU6nzLr1G8bkSJRUtMpNro5bG9mNcyEm3vIwdAo4UzqrwVXCq+pFj1mM/TxaqOjWOVp7FtpjcdzuAE3E3noqNC1jITBje4Myj6d3sbyLwZfCaFSwzzYNAkQyU7QuWXD0sIu0iZZGxRMIBCmyiVxNcIN5g4zEu53sOn7zoqtGblZo4jiqjRdfxANjRzNzMtUhVEpRfkylP4G2xZO0j4jHnArCrLIcmyTc85GWWE8IWIrllgsvaUq1AqljsBfcD01ibrYGTxriD0rFACFuXuDoo1vfbr+0R4/2lXDCnmpuS4uuUg2tbQn1+3KZXGONFxUJdQGyKKdmz/Dtq5JFrE3Hoekz+J45cWiqBcoQyk3AWwI13PhPLfqMvuNvpvX28G6xpqo3df2Vx3HaFZ2cVXRgCMuQqGC7ZXD92+hsRE+GViXzFg6AWAbMpuQcptuRe0ycBhkR2RnKHTdS199jfTkfWdFg6SI4cG9iGAaxFvMSM77ryY8Kex8cRqs1i4sO6wp6KAOQ5+FyeU6vD0kCDIcyn6r3JI0N7m9587xeDfMtVdULAaAnnYka9L7TsuFYsKRSHeY97KoUd23zaaX26Reny8Mi3d6+xrKMXbTNJkgWpxpXDbevh4GUYT1k0+jESenFalKaTrFnWOwMypSgQ7KbqSPKaDrFnSLRSbGcJ2gqJ83eH3m3Q7Q0mFybHpORqU4DJ4RlKVH0NXAMbp1LW6GZNSoC1xzNvaaI+WRezZrQ8WAF+Uzq/H6KXBYEjkNYalVieM4NQq6lMrfzLof7wlya+kqHC/qsUq9sUHyoTF37bn/y/vKV+yP8lUeTD9REn7JV+RQ/8rfpOaUcr8v8HZB+n+F+TQTtsv1IRHcP2rovztOdbsjiDyT/ANf9pVexVY7ui+pP6TLhnX6ZP8o0f/lfa/hnd4fGI/ysDGA85XhfZ0UTdsQzW+lRYfe83ziwNF950YJZnayJfdeTizLGn/jdinam/wAJSpswYTmMNxCuCRmM6jHOGADc4iuGW50mr29GcetkYbFVmGrGamBDm7OxsPzBUE2FozX7tM+3vKiiZMRxmILnT0iVoa0C80SowlKy7SUMox0lVeDZIysIsCjQixAFUS4lEEl6TciVHOwBP3v+ImMszAC5IAG5Og95yPbJWKisrI6INEI7w5M4JNmt0jHafHMt6dyFFmY3ALCwIXlOQpcdwyqwqbm5N8xJHQWBtt4Tiy5nK4xV7N4x4NSfkz8JiPi97W2q68yLdeWphTTzVUpIVV3sbA2CqN2cCw8po4BRWRXH+mjFiFtZsoJAJPIHlzieIxnwWdKC2z3/ANTLZiALWY7ne/recnK5tef9Grhla5XSfSMbjzGm65WJKllBIAJsTq1vATrOC8ZqMlHKyK2UaOAQcosbHxtpeYvD+JFGdiAuJXYvYq6Na4BGmuXbxPjAVuJUXJ0FIk/IqEKp0JZWA6gnlvKyQ5JRa68oiGThqdnXDFq9QBwqKSwOW4XMwOtttdpmY6jVoOrHU5tGVrG2o0YbdLGZvD6zC7sxamCqlmsGYnYAc/Pwne4eiKhKPTV12ubZrjmpvppfacMrwy0OSWWVJCPBsb8P/wARgVYdyw+U31BsNN9d5vhwwupBHUTH4jwyktnVao1sbWNr6Etc3t1PKYWC7RtTZqbkKiuwbML230DaDTSeh6X1dxqtfsRPBKLpbOwcxWpMfB9oRUV3ugRCLd7vEdbHwiuJ4i+cujXUnRTrpccvT7zofq4J1TMHo2ngHlmbQE72EA7zpsCriCKyzPKZ47HR1GDFwD4H8zWRtJl0TlA8Y9TBMhHUwqmxtDK0Xc6yQ8qyWg+eeNUwBeDd4WKg74gwD4k9Yu9SLs8VlUMtVhKRiaG8apaQTCicQLuIQLvJqLqDCKv4lCDUtLQjDOrLz5ee4gkME9XI9+oH2jRMuhRhFqxmjjkupdBc27y8/MTA/iiTYyrMGhzEPraBNQAXJsBvIxr2It01mH2gxNqLdNPaQ3VsaVtI0anaFF0VS3iNBHcF2hoE2e6nqdR9tp8+weMD2RFbUas3y28I6yoNC6E66A66a6gCcizyT2zu9iFaR2faPtC+HRSgUh/kKnu2Fvme3mdOkyq3HsRRUYjPRqU7BmpqSzFWtbIx563v4TncZxQmn8MkGmNQTY2JB1BPyj95i4jjqZDTAapdSBlGin6R5SXKcpXHZk8Ljs6btFilxVqtLVArOeWi6FWHmLeZnP47G0gqL8BAw3ZVPe5kHXa53NzrK8DpslJ2bLmYqQpubAkXuAdCelpergVdCXDI6aobZcyNoB7j2PhM6UZbetm/tSbT+B6pic6g2IUkkINSbW7vsBtD4emKi2RAoUWNwTrbUkKLk/jr0xMJRYq2VzmUXKHQmw1yAElvtGMFxbENlPdKj5m1zC2yk3Fr+szeN19NF5Jxa+rwa2NFJaILKGZSU7wAa1r3K3vYcvWYfEEVVDKRlsDcWFumnIxqpji9QKVuN210FwbKOsQ4vw4mkX71gws17WvuDbyPlDHBxaUjnyy9xKlr+yRUd0CIT1tckk2t6CfQOCcSzKjG+yh1tqjhQHUf0ncHznyTD0mXM5Zu6LrqdTy9J9C4PhDXpUqqnLUAs4vYga3Yga7ReqhGKXxf9lcLSrTXR9BoKjq9EtYkkjyO3mLT57xfs+aTlSPmViRcWY30tfcbHrrCr2jqCug+DZr2ViTmZVGjKux08zEu2/aQVBRdEcOjElnQqUUqCVvc88p9PGThxyaVaf468G7aUtv/AKc3jMD8NSTe9wMnXp5/3mhgOGVFzWdgFC3U21uLtbS4tcC146cUldEJF2Rgw66kGzeFxPcRRFqtplbrclWuL8jp0tNPcb01vyZSjHntaN0YgBRc+Bzd03HUQLVgdiD5GYfEa7NRzIMwU3ZQSWFtO6OY689JgL2gA1UEeonXhyOUeutGWTFG20+zuC8rnnL4XtKGZVZbkkC4035zc/iB1E3swca7Po6UhpGVg0FzLXteOjWzzkQNRrHeRmOkHiVDG3SS2VRY1IJ3mdiKlRDoucXA8dYnX4xkNmR7joLyeQ6Nhmngs5yp2hOoWk5PlaBfiWJe2VMgJt1MYHWUxc2jjWFhMbBYdwBcknczTw63POUhDb20hGP4nlp6Qgp3OnSUSVojSCxtI2DdDb3mhTogC0piALFTz2kuQcbMpKxU3EHicHTq94dx+o+Un+ofqJDixtIvLTMmhDimFZAXfRbasDdbzk8ZxRWDIq5yV7vQk35dNJ3aYpl03HSJV+HYapm7nw2axZ6fcJI66WPtInGT/SxwUU9nzr+Eq3CMoRAgJy/IW+q55G5gcJgqCMzOza6ZbgL5Cw097ztcZ2QYqfhVQ4Owfu+ptcH2E4vifZ/H0yxagGXrT10/4k2nOsU92dayRrTs2h/Dk3su2++21rnTlFMVQQKWQKzbgHW/UDoZxtTFunddWUg7MGEvQ4tU0CsSPKHtSQ1kizUGPs+bJtuAozDmDp5CGocd+I1qgPxBcZQCF1IFpnVFeumcqL3yqBZOXzG29hsPe8Y4TwKqrhidyBbre3O8mUYU3LtExnLnSeh7GohdWZsoUqGykgjWxsRsRe8bwGGVlujG1mDGw1bN8w8dfvMHiPCat2spU5zfv3A11M6Tg2G+CgS9yBcm17k6+m8iVcFTNuKlJprQR6YQAEXtppbmbDfeMY3EU6VJ0JNyjsUJ1Lm1ttzt7wlFMwsddwNNL8rdBMzjmEptUuzEhUQFV5ncKdSWvpppvM203vovjS0tnOuBUObIVBHzXy3sADl5Wvcek6rs3jQlZGJIBGUna4ZbW8dTMHiGKZ2zZRTVVChQcwst7Haw32E3+AcLqOELoFRbDM1hoDcEc2k52nC318WcM4T5pLdHR4pFWyMBr8uxupv3b+cycXTLMyURTCsctRGzLnVgQ2VtlbffTWb3E8Hh8ozsERQTcEqAT42mZQ4JRrG5zMp+rUjzBYa+gnDilVP4/J6EoRknZzVTgTYfOVuzrYp3s3cGpVytlJAtqOnuReLIQ2dNSoU5htfTQjY356Tsa3CFFFloKcxTujWxNtF025CYGG7FYqsO8gQGxIZre4W5noxxzzbkv4MnKEfJnYLC6nLnYbi+oFvEbjbec3iuEI1VlHzMQyhb7Nyt5gz6zwj/ALPRTsatd20tlVsi26cz+J02A4NhqGtOmoNrZrd426sdTOvFgnHtnPmyRkqifIez/wD2c13ZXcfDUa3a5J8Qm49bT6RhuxGGCgOMzcyzEH2Gk6XN008pFp08Uc1makpXXTSLpjMzOnyut7c7jk49xp4iZ74p3QqTlqUjc252025319vGSzRM0812I6WlHTQnqYvgMUrpmOjZsrDowF/Y7jzh3buny/JkMtM8KQPuD7RdEDOxI0Bt9o5bfzt7CL0k0J6tz8pLRVgkoLdu6N+kdo4ZVFyNTAqCTbxB/e8PnJJHIaRoTGAB0lUFjpz1kLe2sgDvDylEjyLpDrYbSlEWWWMTYJEPUtAEXNzK3ubwxXSIoz8fSsb8j+ZnZ7ToXph1Kmc9iUKkgxxZnKIJ3gyZRxKZppZkXLEbEiWXH1F+q/mLwJaVMYDNTiCuLVKSOPEA/ZgYr/CYA74ZFJ/lUDx+m0o0G0T32Oy+J4DgKi5LsgvmsrW116g9YpguxWFSqtVMRUJW5CsylfYAQxtK2ElRjVJApNdDVbsyjEkYgi+puoPO/WB/7om91xAv/svfz70qohkElYYLSRp7015CU+y7C3+uNLbJ+NYgOwgNR3fElixvqmoGwF73M008z7w6xrDD4B55vyZdDsHRHzVmfUHVE3E2aPZ+mpBNWowF+7mUL62F/vLoIwgieDHLtJgs0/kkcKw1rFMwIsQxLAg+EfoJTQBVQADYAAWiyQ6SlihHqKX4JeST7bGlq9FEt8VuvtALCrNCCwlhIEm8AJnryJGeAHHYivnRMQnzL846W0Knwvf0N+UHWJslZdS1wy8yL6qfHl5hZCJ8Ko9M/JUGl/5raj1GkvhkFKpkfVGFtdgW0F/ax8QDzkNGqC4llRlrobo4GceG+a3UXJ9xNRSGFwbqQpBGx53/ABMujlR2pvqhLAH+o7e9vcGTg6hpOKbaIx7hP0sdch6A8oNWNOjXvoB49YJhlTz/AFkhTdfDNeTiSDlXz/vIZSKUU1Zh4A/55RhCCNNryadGynXnf20i+EFkN+bc/T94dB2MAaeclV7w84QiQlgxPX/P0jAfBkPsfKQJ7NJABTh1MAumkuDAAximPwwcafMNv2jAaVeAHLVkKkgwBadBjqAffRus5/EUipsYKREolSZQmULT2aUpEUeZpRmkkyCI+QqKXngZOWTljsRKmHQwKrCosEwoYQw6GLoIdBKsQwhjCGLpGUgNB0MMpgUhVMYUGUwgglMsGgAYGTmgc0qzxNjoKzwBeVWoDLTJzvo0UK7Of41RziwOqgtfptY38P3gKDCvTJb510I535j15dCB0hqrkZm8So9Tb8A+8znU0HV90dVzfv8A54dZSdjaobpAOhU6sut9iynW4vz2PgR5wtT/AFUyNqw3PUW0cfb/AAwNYhWDLzF/C5Juvkd/O/US1R7EVF2J/O6+v58xGJjXCcYT3HPfUHX+ddgw8Y27jOCOja+wmJiKVgKiHY3v/Lc8/Dr79ZpYGqrXdtMq6p0IJJI8DE0CZuJT7tjEUFrA9T66AAxvPe1gevTltFGcFundGnnr+kTKiHB2A/wdZ5xZvUH+0mmBb0/wSlXmfL7GAxsPbylybxF6vcufD7m0mjieu3WTIEMuJGaWBvKssBkZrSc0oTAsxHlJboaVhKouJk4xSN9us0g8pUQNIe+gWjmapA308eUHa+00sbgOa+37TAxOFddUJU8x+4iUmuwcU+hwiRaZH/VXTR0uOq7+x/eMUeN0W0LZT0bu/nSXyM3E0BJEinUVtQQfIwqiNSFxPLCrIVIVUjUhcSUhllVSFRZXIniEWHQwKiFUyuQcQ6mFDRYVBIOJXr7axOaQ1BscDzxqRE4gnYShUnnM5Zkui44m+xv+LBOUHWGGu8z/AIF9/Qw9J2U2bbkf3mSySk9mvCK6GWpyLmEDwZaapE2Yzi5yaWsL/wC4ty9oLHpnyoLWsLX28R5WnqKkF2vuSBz5/t+ZT41rZuQUeZbp42vLEK4R7qyEX0NuR02HgQfuIXDOe8jaEjY7EG9mt0NvTXpK4lcpFQbfUByA0zeP7CM43BZwKtP5wLg8rbkEcwdPLeWtkNUCwzFWNJ/qGh/mGmo8RfX++lqaGg4B1RiFU8rn6D4dD6dLyipjKV0Yo6Hr30ccj+Qdj4iN8PpvXpvSxNMqy2Ba3de40dDyPUcvGUI1GcgAr/h2kUqN9T5a76f/AJBYZfgIVq1c6g9wsO8Et8rH6zvrv1vvFn40hIVFd9dSBtbzkyQ0x9z9PM6+Qva/5lcQ1xbwP+feC/jUdSyNcoygi+oLaZT73l35jnoB67+PhJKBuwNM9LE/k/pFy5W0uPlYafJbwGlv89JU0UKa/LkHtYSWrKTGKGKtsfSP08Qp8JzLVsjFToBYKb+A+b1JF/CMpiSN5HQ6s32SCKxChxC3PTodo4mNRt9PuIrHRD0ukpaNIwOxB8pJS8NMWxNlvEsTgA2o3ms1DppKmiYONjs5PFcN5MPWY+L4Crcp9BejfcRZ8ADsBFxa6DTPl9XgDoboSPIkfiDy4lNqj+tm/wDkDPpr8P6iCfg6nlGKj54nEsWv1qf9yfsRGafG8TzFM/8AFx/9jOyPAh0Ep/0BekBUc5S4ziT9Ce7RpOJYk7LTHo5/WbycEA5RlOFgcoCowadfEtu6DyQ/qxjlOjUPzVG9Mq/gTaTh9uUMuFhTHSMqjhOtz5kn8x5MOI6uHhBTtFxHYmKFpcJ0jgWVZIcA5CplHMcGHl1wyjxhwHYqt5Pwj/NGzTlbCW2TRzOI0UDq1z5Xv+0rUUFE8wxv0XS32M9PSxLoYq0LKRoNDfpoCT9yZn4F6uGUMVL0iAzL9SXAOZRzXUaT09KJGaPFMMrF6KqXcDMwyrcA3AJNuZOkHiu0Fh33VF/pIc/+03+0mej5MTRzuL7W0VJBZn8SqD9C8Ww3aymCLU732+cXHnvPT0TZSR0HDuNYdh3kZM27AkqSeZvz8xOlpMGXOjZwelr+3Oeno0IAhBDAHYHw12/QSpQrT8gijU9ReenpLKKJhg17jQsSb79QfxEMRTamoYaruBcXA1Nl66cpM9JZQGlilcXU36jmPAjlC/Gkz0yK8BFrcwf0MbpcRcfVfz1+8megA5T4uv1L7RqnxCm31W8xaeno0JjKMh2IPrLGmJE9GmJnskqaAnp6MDy05cUQekieghMkYcSwoienoAeZBK5RInomCJFuk9aRPRWyqRBWUYjmRPT0BlHqW21lGqPysPS89PRgUOcj5j7AQXwP62956eg0Kz//2Q==",
		"price": { "amount": "3.25", "unit": "£" }
	}
]


settings = {
	'local_URI': 'http://localhost:7071/api/' ,
	'cloud_URI' : 'https://izifood.azurewebsites.net/api/' ,
	'func_key' : 'xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==',
	'db_URI' : 'https://izifood.documents.azure.com:443/',
	'db_key' : '1mhshxYihKMiJFclc43fCg50GHunrnQVCPh2Na1aI68CCVDaa1kjOiRxCDJycbOGWqew8bP4iiDZACDbbqx1BA==',
	'db_id' : 'izifood'
}


cos_client = cosmos.cosmos_client.CosmosClient(settings['db_URI'], settings['db_key'] )
db_client = cos_client.get_database_client(settings['db_id'])
recipes_container = db_client.get_container_client('recipes')
users_container = db_client.get_container_client('users')

for r in recipes:
	print(r)
	recipes_container.create_item(
			r,
			enable_automatic_id_generation=True
		)