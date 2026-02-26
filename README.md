# DriveAway </center>
## A booking app for Campervan owners to connect with Driveway owners to find safe spots to park up

This application allows people to list their private driveways for campervan users looking for cheaper, more relaxed alternatives to traditional campsites. In the scope of the project, I have designed a view page for all listings either in card format or displayed on a map, a booking system and a minimal messaging system. This allows driveway owners to accept or decline bookings and communicate with campervan owners to organise payment and provide further contact details outside of the application. This application does not take payment for the reserved stays. 

![Website Mockup on Multiple Devices](static/images/websitemockup.png)

## Deployment Instructions

**Live link to the deployed website through Heroku**: https://driveaway-e8200983e2d1.herokuapp.com/

**For Local Deployment:**

1. Navigate to green Code button on main repo page and copy link for clone repo.
![Clone repo step](static/images/clone.png)
2. Open VS Code or alternative IDE and follow instructions for cloning a repo, using the link above.

3. Open a terminal in your project directory and create a virtual environment:
   - For Windows: `python -m venv .venv`
   - For Mac/Linux: `python3 -m venv .venv`
   - Activate it:
     - Windows: `.venv\Scripts\activate`
     - Mac/Linux: `source .venv/bin/activate`

4. Install dependencies:
   - Run `pip install -r requirements.txt` to install all required packages.


5. Create an `env.py` file in your project root to store environment variables.
Do not push your code to github until the next step is followed, to avoid spread of sensitive information.
   - Add the following (replace values with your own):
     ```python
     import os
     os.environ.setdefault('DATABASE_URL', 'postgresql://yourpostgresql-api')
     os.environ['SECRET_KEY'] = 'your-django-secret-key'
     os.environ['CLOUDINARY_URL'] = 'cloudinary://your-cloudinary-api-key:your-cloudinary-api-secret@your-cloud-name'
     ```
   You will need to set your own secret key (can be generated online) and sign up to Cloudinary to get your own API. You will also need to get a PostgreSQL api.

6. Set up a `.gitignore` file:
   - Ensure `.gitignore` includes `.venv/`, `env.py`, and other sensitive or unnecessary files.
   - Example:
     ```
     .venv/
     env.py
     ```

7. Run migrations:
   - `python manage.py migrate`

8. Collect static files:
    - `python manage.py collectstatic`

9. Start the development server:
    - `python manage.py runserver`

10. Open your browser and go to `http://127.0.0.1:8000/` to view the site locally.

## User Experience Design 

I based my user stories both from the view of a driveway owner and a campervan user:

1. **Login Page/Authentication**  
As a user I can create an account so that I can browse listings as a traveller or upload a new listing as an owner.  
 - [ ] Initial Login Page shows when website first appears
 - [ ] User is prompted for details:
     Unique username
     An email
     A Password

2. **Traveller List View**  
As a traveller, I want to switch to a list view so that I can compare driveways by price, facilities, and reviews.  
- [ ] User can toggle between Map View and List View.  
- [ ] List view displays driveway cards with:  
  -Thumbnail image  
  -Price  
  -Rating  
  -Key facilities (toilet, quietness)  
- [ ] Sorting options include: price, rating, distance, availability.  
- [ ] Filters apply consistently across both views.  

3. **Multiple Driveway Upload**  
As a driveway owner, I want to upload multiple driveway spots so that I can list all the spaces I have available.  
- [ ] Owner dashboard allows creation of multiple listings under one account.  
- [ ] Each listing has its own photos, description, facilities, and pricing.  
- [ ] Owner can set availability per spot.  
- [ ] Listings can be edited or unpublished at any time.  

4. **Driveway Owner Facility and Stay Rules**  
As a driveway owner, I want to specify facilities and stay rules so that travellers know what to expect.  
- [ ] Listing form includes fields for:  
  -Toilet availability (yes/no)  
  -Noise level (quiet/average/lively)  
  -Price per night  
  -Minimum stay  
  -Maximum stay  
- [ ] System prevents publishing a listing unless all required fields are completed.  
- [ ] Facility information appears clearly on the listing page.  

5. **Traveller Booking**  
As a traveller, I want to book a stay directly through the app so that I can secure a driveway spot for my campervan.  
- [ ] User can select check‑in and check‑out dates.  
- [ ] System validates dates against minimum/maximum stay rules.  
- [ ] Booking summary displays price breakdown before confirmation.  
- [ ] User receives booking confirmation via in‑app notification and email.  
- [ ] Driveway owner receives booking request/confirmation.  

6. **Map View**  
As a traveller, I want to browse driveways on a map so that I can quickly find suitable places near my route.
- [ ] Map view displays all available driveway listings as pins.  
- [ ] Pins show price and availability on hover/tap.  
- [ ] User can zoom, pan, and recenter the map.  
- [ ] Filters (price, facilities, noise level, dates) update the map results in real time.  
- [ ] Selecting a pin opens the listing preview card.  

7. **Traveller Review Visibility**  (Not Complete)
As a traveller, I want to see reviews on each driveway’s main page so that I can judge whether the spot is trustworthy and comfortable.  
- [ ] Listing page displays average rating and total number of reviews.  
- [ ] Reviews section shows: reviewer name, date, rating, and written feedback.  
- [ ] Reviews are sorted by most recent by default.  
- [ ] If no reviews exist, a placeholder message is shown.  

8. **Traveller Review Submission**  (Not Complete)
As a traveller, I want to leave a review after my stay so that I can share my experience.  
- [ ] User can only review a stay after the checkout date.  
- [ ] Review form includes star rating and optional written feedback.  
- [ ] Submitted reviews appear on the listing page after moderation rules (if any).  
- [ ] User cannot submit multiple reviews for the same stay.  

### Wireframing for User Stories

![Figma WireFrame of Project](static/images/DriveAway.png)

## Agile Development Process

User storiers were mapped on to a Kanban project board, giving each story a level of priority from could have to must have. This gave me room to adjust the scope of my project as time continued to ensure a Minimum Viable Product, or MVP, was delivered. I created three status columns, to-do, in progress and done to monitor the progress of my project.

![Kanban project board with my user stories listed with priority given](static/images/kanban.png)
[Project Board Link](https://github.com/users/livlockyeardev/projects/9)

## The Design Process

I took inspiration from sites such as AirBnB, using modern sleek fonts and minimal colour. I drafted an idea for my design using Replit with AI prompts to match my design ideas.

![Replit initial design idea based off AirBnB](static/images/replit.png)

This led me to settle on the following colour scheme: 

![Colour Palette Selection](static/images/Copilot_20260224_180202.png)

And the following minimal font as a logo and as my main header text:

![Font Selection](static/images/font.png)

## Database Design (ERD)

Next I needed to design the database structure, how my data would be held and which data types would be keys to link to other tables of data. This is known as an Entity-Relationship-Diagram or ERD:

![Entity relationship diagram for my campervan user app](static/images/erd.png)

## Use of AI 

During this project, I utilised LLMs to help me build my application. I used Microsoft Copilot for image generation, development of user stories and specific acceptance criteria. Furthermore I used the built in chat function within Visual Studio (primarily model GPT -4.1) for:  
   -  **Code generation**  
    E.g How would I implement this feature step by step?  
    Example in Code: AI used to determine logic of block_off_availability function
    Led to use of decorator to authorise user is logged in as well as implementation of try: and except: logic. 
   -  **Tutor support**  
    E.g What does this line of code do? Or how does this function work?  
   - **Debugging**  
   E.g Fix my syntax error from line 34-56  
   -  **Building Automated Tests**
   To test for edge cases of my front end CRUD functionality forms (9 tests generated)

While incorporating this technology no doubt made me more creative with my project and immproved my efficiency, it often led to repetitive or overly complex solutions that I had to later streamline.  

## Testing 

### Manual Testing
For testing of my website, I first manually tested each user story  
**Results**  
Each user story, designated as high priority was completed but certain features, such as the ability to filter and reorder listings based on certain qualities, could not be implemented in time.  
Two User stories, designated as low priority, relating to user ability to leave reviews of past stays, could not be completed in the scope of the project. Nonetheless, the ability for the owner to send a message to the user making a booking allows for further communication outside of the application.
 
### Automated Testing
I then implemented automated testing, designing 9 tests to test for edge cases for my forms in listings and bookings apps.  

**Results** 
![Automated testing result](static/images/automated.png)

**Lighthouse and Code Validation**

Finally, I then generated lighthouse reports and validated code:
![Lighthouse and testing report for my application](static/images/testing.png)

**Results**

Generally, accessability and performance scored highly, but I scored lower points for best practice in pages that included Cloudinary sourced images. This was due to Cloudinary setting an insecure connection (http instead of https) for each image. This is unadvisable as it makes a website easier to access maliciously. While I tried to alter the code, I could not fix this detail.
All code was validated without errors, with one remaining regarding the use of an aria-labelledby attribute in a form. As this is spontaneously generated code, using the all-auth application, I was not able to locate the form code to adjust its attributes.

![Error remaining in code validator referring to accessibility labelling](static/images/remaining.png)

## Credits

External code was utilised to implement calendar functionality and map generation.

**Calendar**
Generates a UI calendar display for the user to see when the listing is already booked. Code adapted from FullCalendar library ([Link for Calendar Code](https://fullcalendar.io/))

