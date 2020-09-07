[![alt text](https://res.cloudinary.com/dm2vu1yzr/image/upload/v1599469933/name_s81qy7.png)](https://dashboard.heroku.com/apps/recipme-pe)

# RecipeMe

RecipeMe is a CRUD based webapp for users to create, save and share their favorite recipes. All recipes on the app are user created and as such all data for the application is user defined. Users also determine the popularity of recipes via ratings which directly affect what recipes are displayed on the home page, who the highest rated user is and the ordering of search results of recipes.

## UX & FEATURES

### User

As a user, I should be able to..
* Create my own recipes
* Create an account to long term storing of my recipes
* Share recipes with other people
* See other peoples recipes
* Rate other peoples recipes
* See other recipes by my favorite users
* Edit my recipes
* Easily copy people recipes and put my own spin them
* Store favorite recipes
* Edit/Delete my account
* Edit/Delete my recipes

### Design
This Project is designed to allow use to conduct basic CRUD (Create, Read, Update, Delete) actions on a database. The database utilised for this app is [MongoDB](https://www.mongodb.com/what-is-mongodb), more on this [below](#Database) . The Frontend of the project is mainly [Bootstrap](https://getbootstrap.com/) as it is modern, responsive and a template style alot of web user would be familiar with.

**Database**
For this project I used [MongoDB Atlas](https://account.mongodb.com/account/login) to host my 


### Wireframes
<img src="/assets/wireframes/wireframe-mobile.png" style="center" width="25%">
<img src="/assets/wireframes/wireframe-desktop.png" style="center" width="40%">


## TECHNOLOGIES USED

### Languages
* [HTML](https://en.wikipedia.org/wiki/HTML)  - Struture of the page.
* [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) - Style of the page.
* [Javascript](https://en.wikipedia.org/wiki/JavaScript) - User and API interaction/animation.

### API
* [COVID-19 Free API](https://rapidapi.com/api-sports/api/covid-193/details)

### Libraries
* [Bootstrap 4.5](https://getbootstrap.com/)
* [Font Awesome 4.7](https://fontawesome.com/v4.7.0/)
* [JQuery 3.5.1](https://jquery.com/)
* [Datatables 1.10.20](https://datatables.net/)
* [Select2 4.1.0](https://select2.org/)
* [Popper.js 1.16.0](https://popper.js.org/)
* [Chart.js 2.8.0](https://www.chartjs.org/)

### Tools
* [Github](https://github.com/) - Repository Hosting.
* [Gitpod](https://www.gitpod.io/) - IDE.
* [Google Chrome developer tools](https://developers.google.com/web/tools/chrome-devtools) - UX Testing.
* [Responsive Test Tools](http://responsivetesttool.com/) - UX Testing.
* [W3C - HTML Validator](https://validator.w3.org/) - Validate HTML.
* [W3C - CSS Validator](https://jigsaw.w3.org/css-validator/) - Validate CSS.
* [PurifyCSS](https://purifycss.online/) - Remove unused CSS.
* [CSS-beautify](https://www.cleancss.com/css-beautify/) - Format CSS.
* [Loading.io](https://loading.io/) - Create loading image.
* [AutoPrefixer](https://autoprefixer.github.io/) - Add vendor prefixes to CSS.
* [Codepen](https://codepen.io/) - Isolated code testing.
* [Figma](https://www.figma.com/) - Wireframes.

## TESTING / ISSUE RESOLUTION

Each section has had extensive individual testing across multiple browsers including the use of chrome developer tools & [Website Responsive Testing Tool](http://responsivetesttool.com/) to test on a wide variety for sizes and aspect ratios, please see some key points to note below:

1. Responsiveness - alot of consideration had to taken here as the javascript generates HTML code, therefore the responsiveness had to be tested on every button click and multple combinations of button clicks. For the most part I beleive this testing lead to a responsiveness level that I'm content with, my one outstanding responsiveness issue is with the graph, in order to see the enitre graph the user needs to scroll the page horizontally, I would prefer it to be like the table where only the table scrolls to fit data but when trying to use this approach I came into scale issues with the graph that made it unreadable.

2. Dashboard layout - due to the way i setup the dashboard style page using column/row combination I had to adjust standard bootstrap container sizes as the standard ones would push the content (API data) below the sidebar as they wouldnt factor the space the sidebar took up on screen into the flexiblity of the content containers.

3. Single Button Spamming - due to the content of the app being JS generated via an API I ran into issues of button spamming (multiple clicks of same button) so I had to develope a way to prevent large numbers of requests going to the API in a short amount of time, this was resovled by adding a delay to some of the funcitons meaning the button would be disabled for 2 seconds after click. 

4. Concurrent function execution - due to testing an issue arose where rapid click of different buttons would cause multple functions to trigger concurrently which led to disfigured data, this was resolved again by click delay functions and also for the table click (which takes the longest and therefore had to greatest potential for concurrent clicks) an transparent overlay would be generated to cover teh entire page until the function was complete, preventing any buttn clicks while process was running.

5. API testing - Alot of my API testing can be seen via my commit history, at some stage in the creation of all of my API JS functions I have various instances of concsole logging to see what data I was getting back from the API and then trial and error to get teh data I wanted back. These testing pieces of code have since been removed for the cleanliness of the code once the funciton was working as hoped.


## DEPLOYMENT

### Deploy to Github Pages

1. Open GitHub and go to the projects **'Repository'**
2. Click **'Settings'**
3. Scroll down to the **'GitHub Pages'** section
4. Click on the dropdown under **'Source'** and select the **'Master Branch'** option
5. A green box should appear with the following message **'Your site is published at.../'**


### Cloning a Repository 

1. Go to the main page of the GitHub repository and click on the dropdown menu **'Clone or download'**
2. Copy the URL and go to your local IDE (Integrated Development Environment)
3. In the terminal of your IDE type in **'git clone'** and the paste the URL copied from step 2 
4. Press **Enter** and the clone will be created


## CREDITS

### Media
- The images/icons used in this site were obtained from [Flaticon](https://www.flaticon.com/) & [Loading.io](https://loading.io/) (See Fair Use Disclaimer)

### Acknowledgements

I received inspiration for this project from the below websites:

1. [Worldometers](https://www.worldometers.info/coronavirus/)
2. [Google Covid19](https://news.google.com/covid19/map?hl=en-IE&gl=IE&ceid=IE:en)

### Code Snippets / References
Below links helped me in various parts of the project to overcome issues:
#### Sidebar:
* https://stackoverflow.com/questions/49641293/bootstrap-4-fixed-top-nav-and-fixed-sidebar
* https://www.codeply.com/go/3e0RAjccRO/bootstrap-4-collapsing-sidebar-menu
* https://www.codeply.com/p/FpImnZeaPt
* https://www.w3schools.com/howto/howto_js_collapse_sidebar.asp

#### JSON & AJAX:
* https://www.youtube.com/watch?v=rJesac0_Ftw

#### JQuery:
* https://www.youtube.com/watch?v=rJesac0_Ftw
* https://www.w3schools.com/jquery/html_toggleclass.asp
* https://stackoverflow.com/questions/12934144/how-to-reload-refresh-jquery-datatable
* https://stackoverflow.com/questions/5000415/call-a-function-after-previous-function-is-complete
* https://stackoverflow.com/questions/10932766/disable-the-submit-button-after-clicking-and-enable-it-back-again-after-a-few-se/10932857
* https://stackoverflow.com/questions/12374356/disable-jquery-function-for-x-seconds

#### Chart.js:
* https://www.chartjs.org/docs/latest/getting-started/
* https://medium.com/wdstack/bootstrap-4-chart-js-39006427f08f
* https://www.youtube.com/watch?v=5-ptp9tRApM
* https://stackoverflow.com/questions/39723147/change-x-and-y-axis-font-color
* https://stackoverflow.com/questions/35854244/how-can-i-create-a-horizontal-scrolling-chart-js-line-chart-with-a-locked-y-axis
* https://stackoverflow.com/questions/24785713/chart-js-load-totally-new-data
* https://stackoverflow.com/questions/38800226/chart-js-add-commas-to-tooltip-and-y-axis

#### Misc:
* https://stackoverflow.com/questions/9372624/formatting-a-number-as-currency-using-css
* https://stackoverflow.com/questions/4537227/javascript-replace-special-chars-with-empty-strings/4537264
* https://getbootstrap.com/docs/4.0/components/pagination/
* https://stackoverflow.com/questions/46462171/using-the-same-function-with-multiple-buttons
* https://stackoverflow.com/questions/50715991/update-javascript-variable-on-a-html-select-value-change
* https://codepen.io/profoj/pen/abzgpLN
* https://stackoverflow.com/questions/8595909/how-to-completely-disable-any-mouse-click
* https://getbootstrap.com/docs/4.4/content/tables/
* https://stackoverflow.com/questions/39260521/how-to-replace-all-the-zeros-in-javascript

## FAIR USE DISCLAIMER
 - The images, icons and graphics used in this project are not owned by me and I have not been given permission to use these, the purpose of their inclusion is purely for visuals within the project and the entire project is for nonprofit educational purposes. If this site was to ever go outside the remit of "nonprofit educational" then these images would be removed prior to such action.