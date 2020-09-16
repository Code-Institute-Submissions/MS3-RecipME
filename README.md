

[![alt text](https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599469933/name_s81qy7.png)](https://recipme-pe.herokuapp.com/)

  

# RecipeMe

  

RecipeMe is a CRUD based web app for users to create, save, and share their favourite recipes. All recipes on the app are user-created and as such all data for the application is user-defined. Users also determine the popularity of recipes via ratings which directly affect what recipes are displayed on the home page, who the highest rated user is, and the ordering of search results of recipes.

  

## UX & FEATURES

  

### User

  

As a user, I should be able to...

* Create my own recipes

* Create an account for long term storing of my recipes

* Share recipes with other people

* See other peoples recipes

* Rate other peoples recipes

* See other recipes by my favourite users

* Edit my recipes

* Easily copy people recipes and put my own spin them

* Store favourite recipes

* Edit/Delete my account

* Edit/Delete my recipes

  

### Design

This Project is designed to allow users to conduct basic CRUD (Create, Read, Update, Delete) actions on a database. The database utilised for this app is [MongoDB](https://www.mongodb.com/what-is-mongodb), more on this [below](#database) . The Frontend of the project is mainly [Bootstrap](https://getbootstrap.com/) as it is modern, responsive and a template style a lot of web users would be familiar with.

#### Wireframes

For this project I used [Balsamiq](https://balsamiq.com/) to create my initial frontend design using wireframes, very basic setup was done initially and the wireframes were updated as the project progressed along with my vision for how I wanted the app to look.

##### Home

| Desktop / Tablet      | Mobile                 | 
| --------------------- | ------------------------ | 
|<img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599469893/Desktop_-_Home_pxnxue.png"  style="center"  width="100%"> | <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599469893/Mobile_-_Home_xr5z6a.png"  style="center"  width="100%"> |
 
##### Dashboard
| Desktop / Tablet      | Mobile                 | 
| --------------------- | ------------------------ | 
|x<img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599469893/Desktop_-_Dashboard_j0jgtp.png"  style="center"  width="100%">| <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599469893/Mobile_-_Dashboard_j68gyr.png"  style="center"  width="100%">|
 
##### Recipe

| Desktop / Tablet         | Mobile                 | 
| --------------------- | ------------------------ | 
| <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599469893/Desktop_-_Recipe_bcwdio.png"  style="center"  width="100%"> | <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599469893/Mobile_-_Recipe_b6lbaa.png"  width="100%"> | 

#### Database

For this project I used [MongoDB Atlas](https://account.mongodb.com/account/login) to host my database, see schema below:

 <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599475537/Schema_-_Full_adwzjb.png"  style="center"  width="100%">

### Features

#### Navbar

Stored on the base.html file to create consistency across all of the pages, provides quick access to home, spotlight, featured, and all recipes.

Also provides entry point for [account management](#full-account-management) and [search](#search) functionality outlined below.

 <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599476966/Nav_bi150b.png"  style="center"  width="100%">

#### Spotlight

Shows which user is currently the highest-rated and that users highest rated recipe.

 <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599476970/Spotlight_awkwmw.png"  style="center"  width="70%">
 
#### Featured

Shows the top 3 rated recipes on the app.

 <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599476969/Featured_iicnpw.png"  style="center"  width="70%">

#### Search

Allows users to enter a term(s) and return results based off of the entered data, the search creates an index to check against recipe name, description & ingredients 

<img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599477745/search_il0m5y.png"  style="center"  width="70%">

#### Full Account Management

Full CRUD actions available for a user account, and [Flask](https://flask.palletsprojects.com/en/1.1.x/) utilized to facilitate user log n / log out via sessions.

 <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599476608/Account_Managment_ia0xlu.png"  style="center"  width="100%">

#### Dashboard Data

Upon logging in if a user has created recipes they will be presented with graphical data regarding how users have interacted with their recipes in terms of ratings. These graphs show the rating distribution (number of each rating given to users recipes) and most rated recipes (users recipes that have had the highest number of votes registered)

 <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599477850/Charts_pl7i73.png"  style="center"  width="100%">

#### Add Recipe

For users to add a recipe they first need to be logged in, this could be seen as a potential barrier for frivolous users, but it encourages users to be more active and engaged with the app by creating an account.

To add a new recipe the user can simply click the dropdown under their name and select "Add recipe" from anywhere on the site, this will then prompt a tabbed modal to appear where the recipe can be added in three sections, images can be added after the recipe is added.

 <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599478300/recipemodal_l2gb5e.png"  style="center"  width="100%">

#### Edit Recipe / Copy & Edit Recipe / Delete Recipe

When on a recipe page:
1.  The owner of the recipe is presented with an option to edit a recipe that will bring the user to a new page similar to the add recipe modal, where whatever is already in the recipe, will be populated and available for editing. They also here have the option to upload an image for their recipe here. This works through [Cloudinary](https://cloudinary.com/) API, if there is no image a new image will be uploaded to Cloudinary and the image URL will be stored in the database on the recipe document, if an image already exists it will delete the existing image, upload the new image and update the database will the new images URL. Also, only the owner of a recipe will be presented with the option to delete a recipe that will fully remove the recipe and all ratings for the associated recipe from the database.
 
 <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599493670/upload_image_ewmd3n.png"  style="center"  width="100%">

2. A signed up (not-recipe owner) user will be presented with the option to copy a recipe, this fundamentally work very similar to the edit recipe except this does not overwrite the original recipe, it adds a new instance of it with a new ID and the author/owner of this new version is the user who copied it.

 <img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599493331/edit_copy_recipe_zv70zy.png"  style="center"  width="100%">

3. A non-signed up user will only be able to view the recipe, attempts to do actions that are limited to signed up users will redirect them to the home page.

## TECHNOLOGIES USED

  

### Languages

*  [HTML](https://en.wikipedia.org/wiki/HTML) - Struture of the page.

*  [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) - Style of the page.

*  [Javascript](https://en.wikipedia.org/wiki/JavaScript) - User and API interaction/animation.

*  [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) 3.8.3 - Backend of app.  

* [Jinja2](https://pypi.org/project/Jinja2/) 2.11.2 - Templating language.

### APIs

*  [Cloudinary](https://cloudinary.com/)

### Frameworks
*	[Flask 1.1.2](https://flask.palletsprojects.com/en/1.1.x/)

### Libraries

*  [Bootstrap 4.5](https://getbootstrap.com/)

*  [Font Awesome 5.14](https://fontawesome.com/)

*  [JQuery 3.5.1](https://jquery.com/)

*  [Chart.js 2.8.0](https://www.chartjs.org/)


### Tools

*  [Github](https://github.com/) - Repository Hosting.

*  [Gitpod](https://www.gitpod.io/) - IDE.

*  [Google Chrome developer tools](https://developers.google.com/web/tools/chrome-devtools) - UX Testing.

*  [Responsive Test Tools](http://responsivetesttool.com/) - UX Testing.

*  [W3C - HTML Validator](https://validator.w3.org/) - Validate HTML.

*  [W3C - CSS Validator](https://jigsaw.w3.org/css-validator/) - Validate CSS.

*  [Codebeautify](https://codebeautify.org/css-beautify-minify) - Format CSS.

*  [AutoPrefixer](https://autoprefixer.github.io/) - Add vendor prefixes to CSS.

*  [Codepen](https://codepen.io/) - Isolated code testing.

*  [Balsamiq](https://balsamiq.com/) - Wireframes.

* [Stackedit](https://stackedit.io/) - Live markdown editor.

* [vecteezy](https://www.vecteezy.com/) - App graphics.

* [GitGuardian.com](https://dashboard.gitguardian.com/) - Monitor repo commits for senstive information(API keys etc).

> Note: Additional dependencies per requirements.txt file

## TESTING / ISSUE RESOLUTION

  

Each section has had extensive individual testing across multiple browsers including the use of chrome developer tools & [Website Responsive Testing Tool](http://responsivetesttool.com/) to test on a wide variety for sizes and aspect ratios, please see some key points to note below:

  

1. Sensitive Data - upon deploying the live version of the site I noticed that my env.py file (containing API keys, Secrets etc.) had been committing to my repo despite being included in my git ignore file, after discovering this my plan was to rewrite the files out of my git history with `git filter-branch --index-filter 'git rm --cached --ignore-unmatch env.py' HEAD` but after consulting with Code Institute it was determined the best approach would be to remove the latest file and change all my keys, which I did.

  

2. User Testing - after deploying the live version of the site I had several family/friends try to use the app without instruction and based on these there was several fixes and updates to be made. in terms of fixes, the most notable was if a user was the "Top Chef" on the site and then delete their account, instead of the next highest rated user becoming top chef the section would just be blank, this behaviour was rectified. There was also a lot of feedback in terms of "expected behaviour", where a user would try click something they expected to be a link (such as recipe name, chef name) it wasn't set up as a nav link, this was also updated.

  

3. Session Testing - this was a major part of this project, ensuring only users who were authorised to do certain actions could do certain actions. Some of the key scenarios for testing were as follows:
`No Account User`  to ensure they only had read the ability to the site, this user cannot add, update, delete any recipes without first signing up for an account and being in an active session. This goes beyond ti just presenting the link to the user but having server site code to detect if the user manual tried to access the functions via manual input of the URL.
`Account User` be able to add a new recipe, rate recipes, be able to be top chef, be able to save other users recipes as for easy access, ensure dashboard populates correctly if the user has rated recipes.**
`Account User - Recipe Owner` to ensure only the owner of a recipe could edit/delete a recipe and add an image for that recipe.
`Account User - Not Recipe Owner` to be able to copy and create their own version of another users recipe without it impacting the original recipe.

>**As part of this testing it was discovered that the dashboard was populating based on ratings given out by the user instead of ratings for the users' recipes, this was rectified.
  

5. General UX Testing - Validating links:

| Element/Link| Linked to / Action| 
| - | - | 
|Logo|Home|
|Spotlight/Featured|Homepage sections|
|All Recipes|All recipes function|
|Sign In|Sign In modal|
|Sign In button|Sign in function|
|Create one button|Create account modal|
|Create Account button|Create account function|
|Password Fields|JS to validate match|
|Password visable icons|Display password on hover|
|Rating Stars|Highlight on hover / Rating function on click|
|Add/Edit/Copy/Delete/Save/Unsave recipes|Linked to appropriate functions|
|Sign Out|End session|
|Edit Account|Edit account modal|
|Update Account button|Update account function|
|Delete Account|Delete account modal|
|Delete Account button|Delete account function|
|Username links|Display that users recipes|




## DEPLOYMENT

  

### Hosting
As this app depending on backend python code it requires hosting on a server that can run this code, there are several options available here such as [AWS](https://aws.amazon.com/getting-started/hands-on/launch-an-app/), [Azure](https://azure.microsoft.com/en-us/free/python/search/?&ef_id=CjwKCAjwnef6BRAgEiwAgv8mQYQ2u3TBwNQaph4w1PVAZ0mpLjV_Ja8FpqxLBB1hcLB261n1nIeUeBoCmRYQAvD_BwE:G:s&OCID=AID2100059_SEM_CjwKCAjwnef6BRAgEiwAgv8mQYQ2u3TBwNQaph4w1PVAZ0mpLjV_Ja8FpqxLBB1hcLB261n1nIeUeBoCmRYQAvD_BwE:G:s&dclid=CMKMnZyr3usCFYNjFQgd1iUP2A) & [Heroku](https://www.heroku.com/). This project has been hosting on Heroku.


  
### Environment Variables

You will need to set up the following environment variables on your system.

| Variable name         | Used for                 | Notes                                                        |
| --------------------- | ------------------------ | ------------------------------------------------------------ |
| CLOUDINARY_API_KEY| Cloudinary Image package | Found in your Cloudinary account dashboard                    |
| CLOUDINARY_API_SECRET| Cloudinary Image package | Found in your Cloudinary account dashboard                    |
| CLOUDINARY_CLOUD_NAME| Cloudinary Image package | Found in your Cloudinary account dashboard                    |
| db_name**| Mongo DB | This is the name of your database collection |
| MONGO_URI**| Mongo DB | Found in the connect button on the database cluster          |
| secret_key**| Flask   | This is a unique secret used for session encryption,  you can use any random string for this |
| IP                    | Flask                    | You can use `0.0.0.0` here to indicate a local IP address    |
| PORT                  | Flask                    | You can use the default port `5000`                          |




**From MongoDB:
1. db_name:
<img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599732673/DBname_rlobu4.png"  style="center"  width="15%">
2. MONGO_URI:
<img  src="https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599732964/MongoURI_atcgyp.png"  style="center"  width="70%">
3. secret_key:
Can be generated in terminal via `python -c 'import os; print(os.urandom(16))'` There is a good answer on StackExchange for this [here](https://unix.stackexchange.com/questions/230673/how-to-generate-a-random-string) which give options to include/exclude certain characters.

### Requirements
1. Python 3.8.3 or later
2. Git
3. IDE (Integrated Development Environment) or code editor

### Cloning a Repository

1. Go to the main page of the GitHub repository and click on the dropdown menu **'Clone or download'**

2. Copy the URL and go to your local IDE

3. In the terminal of your IDE type in **'git clone'** and then paste the URL copied from step 2

4. Press **Enter** and the clone will be created

  
### Installing Dependencies
For the code to run the dependencies will need to be installed, to do this in the terminal use `pip3 install -r requirements.txt`, if updates are made and further dependencies have been added please use `pip3 freeze --local > requirements.txt`to update the requirements.txt file

## CREDITS

  

### Media

- The images/icons/graphics used in this site were obtained from [vecteezy](https://www.vecteezy.com/) (See Fair Use Disclaimer)

  

### Acknowledgements

  

I received inspiration for this project from the below websites:

  

1.  [BBC Food](https://www.bbc.co.uk/food)

2.  [AllRecipes](https://www.allrecipes.com/)

> Also big thanks to [Frozenaught](https://github.com/Frozenaught) & his project [homechopped](https://github.com/Frozenaught/homechopped), which I happened across when browsing LinkedIn, helped me big time to be able to see how someone else was able to tackle issues towards a similar end goal. 

### Code Snippets / References

Below links helped me in various parts of the project to overcome issues:

#### Javascript / JQuery:
* https://www.sanwebe.com/2013/03/addremove-input-fields-dynamically-with-jquery 
* https://stackoverflow.com/questions/46356054/how-to-increment-variable-names-in-jquery-in-a-loop
* http://jsbin.com/moweluwu/1/edit?html,js,output
* https://stackoverflow.com/questions/23700005/jquery-increment-id-number-when-dynamically-appending-elements/23700702
* https://itnext.io/5-ways-to-loop-over-dom-elements-from-queryselectorall-in-javascript-55bd66ca4128
* https://getbootstrap.com/docs/4.0/components/navs/#javascript-behavior
* https://stackoverflow.com/questions/22297964/bootstrap-tabs-next-previous-buttons-for-forms/22298275
* https://stackoverflow.com/questions/4565075/jquery-if-element-has-class-do-this
* https://stackoverflow.com/questions/2727303/jquery-counting-elements-by-class-what-is-the-best-way-to-implement-this
* https://www.codewall.co.uk/jquery-on-click-function-not-working-after-appending-html/
* https://forum.jquery.com/topic/how-to-display-a-message-layer-after-form-submit
* https://stackoverflow.com/questions/48859410/python-how-do-i-iterate-through-an-html-element-object-with-lxml-requests
* https://stackoverflow.com/questions/41107441/onchange-check-password-to-be-similar
* https://www.w3schools.com/howto/howto_js_toggle_password.asp
* https://api.jquery.com/hover/
* https://stackoverflow.com/questions/1544317/change-type-of-input-field-with-jquery
* https://stackoverflow.com/questions/10039968/submit-form-using-a-tag
* https://stackoverflow.com/questions/48613992/bootstrap-4-file-input-doesnt-show-the-file-name
* https://stackoverflow.com/questions/12206660/how-to-retrieve-value-from-elements-in-array-using-jquery

#### Python / Flask / MongoDB:
* https://stackoverflow.com/questions/22304500/multiple-or-condition-in-python
* https://www.geeksforgeeks.org/find-average-list-python/
* https://stackoverflow.com/questions/23025891/flask-pass-variables-from-redirect-to-render-template
* https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
* https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
* https://docs.mongodb.com/manual/core/index-text/#create-text-index
* https://www.youtube.com/watch?v=4QUGWnz-XaA
* https://www.youtube.com/watch?v=Lnt6JqtzM7I
* https://www.youtube.com/watch?v=w1STSSumoVk&list=PL4JDh0LtP7jr0nNuoW-KB-O2uABkaMhL1
* https://www.youtube.com/watch?v=vVx1737auSE&list=PLizxdXKVQPx7XJeP_4AOr746Xvtn4k0GG&index=3
* https://www.youtube.com/watch?v=HyDACIfdPs0&list=PLizxdXKVQPx7XJeP_4AOr746Xvtn4k0GG&index=5
* https://www.youtube.com/watch?v=o8jK5enu4L4&list=PLizxdXKVQPx7XJeP_4AOr746Xvtn4k0GG&index=2&t=0s

#### Bootstrap:
* https://stackoverflow.com/questions/37287153/how-to-get-images-in-bootstraps-card-to-be-the-same-height-width
* https://stackoverflow.com/questions/43816331/bootstrap-4-card-image-zoom

#### Cloudinary:
* https://cloudinary.com/documentation/how_to_integrate_cloudinary

#### Chart.js:

* https://www.chartjs.org/docs/latest/getting-started/
* https://www.codeply.com/go/HRbpJ9qDA8
* https://www.youtube.com/watch?v=5-ptp9tRApM


#### Misc:

* https://tympanus.net/codrops/css_reference/object-fit/
* https://stackoverflow.com/questions/12140961/inset-box-shadow-for-inputfield
* https://stackoverflow.com/questions/26914380/schema-for-user-ratings-key-value-db
* https://forums.meteor.com/t/best-method-for-storing-user-votes-ratings-in-mongodb/39149/2
* https://codepen.io/neilpomerleau/pen/wzxzQr
* https://bootsnipp.com/snippets/GaeQR
* https://www.tutorialspoint.com/css/css_text-transform.html

  

## FAIR USE DISCLAIMER

- The images, icons, and graphics used in this project are not owned by me and I have not been permitted to use these, the purpose of their inclusion is purely for visuals within the project and the entire project is for nonprofit educational purposes. If this site was to ever go outside the remit of "nonprofit educational" then these images would be removed before such action.