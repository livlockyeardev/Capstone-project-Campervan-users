# DriveAway </center>
## A booking app for Campervan owners to connect with Driveway owners to find safe spots to park up

This application allows people to list their private driveways for campervan users looking for cheaper, more relaxed alternatives to traditional campsites. In the scope of the project, I have designed a view page for all listings either in card format or displayed on a map, a booking system and a minimal messaging system. This allows driveway owners to accept or decline bookings and communicate with campervan owners to organise payment and provide further contact details outside of the application. This application does not take payment for the reserved stays. 

## Designing User Stories

I based my user stories both from the view of a driveway owner and a campervan user:

1. **Login Page/Authentication**
As a user I can create an account so that I can browse listings as a traveller or upload a new listing as an owner.
 -[] Initial Login Page shows when website first appears
 -[] User is prompted for details:
     Unique username
     An email
     A Password

2. **Traveller List View**
As a traveller, I want to switch to a list view so that I can compare driveways by price, facilities, and reviews.
-[] User can toggle between Map View and List View.
-[] List view displays driveway cards with:
  -Thumbnail image
  -Price
  -Rating
  -Key facilities (toilet, quietness)
-[] Sorting options include: price, rating, distance, availability.
-[] Filters apply consistently across both views.

3. **Multiple Driveway Upload**
As a driveway owner, I want to upload multiple driveway spots so that I can list all the spaces I have available.
-[] Owner dashboard allows creation of multiple listings under one account.
-[] Each listing has its own photos, description, facilities, and pricing.
-[] Owner can set availability per spot.
-[] Listings can be edited or unpublished at any time.

4. **Driveway Owner Facility and Stay Rules**
As a driveway owner, I want to specify facilities and stay rules so that travellers know what to expect.
-[] Listing form includes fields for:
  -Toilet availability (yes/no)
  -Noise level (quiet/average/lively)
  -Price per night
  -Minimum stay
  -Maximum stay
-[] System prevents publishing a listing unless all required fields are completed.
-[] Facility information appears clearly on the listing page.

5. **Traveller Booking**
As a traveller, I want to book a stay directly through the app so that I can secure a driveway spot for my campervan.
-[] User can select check‑in and check‑out dates.
-[] System validates dates against minimum/maximum stay rules.
-[] Booking summary displays price breakdown before confirmation.
-[] User receives booking confirmation via in‑app notification and email.
-[] Driveway owner receives booking request/confirmation.

6. **Map View**
As a traveller, I want to browse driveways on a map so that I can quickly find suitable places near my route.
-[] Map view displays all available driveway listings as pins.
-[] Pins show price and availability on hover/tap.
-[] User can zoom, pan, and recenter the map.
-[] Filters (price, facilities, noise level, dates) update the map results in real time.
-[] Selecting a pin opens the listing preview card.

7. **Traveller Review Visibility**
As a traveller, I want to see reviews on each driveway’s main page so that I can judge whether the spot is trustworthy and comfortable.
-[] Listing page displays average rating and total number of reviews.
-[] Reviews section shows: reviewer name, date, rating, and written feedback.
-[] Reviews are sorted by most recent by default.
-[] If no reviews exist, a placeholder message is shown.

8. **Traveller Review Submission**
As a traveller, I want to leave a review after my stay so that I can share my experience.
-[] User can only review a stay after the checkout date.
-[] Review form includes star rating and optional written feedback.
-[] Submitted reviews appear on the listing page after moderation rules (if any).
-[] User cannot submit multiple reviews for the same stay.

## Wireframing for User Stories

![Figma WireFrame of Project](static/images/DriveAway.png)