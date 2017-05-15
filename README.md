RoomEase
========
Current build status: <img src="https://circleci.com/gh/kaesackett/RoomEase.svg?style=shield&circle-token=:circle-token">
<h3>Built by <a href="https://www.linkedin.com/in/kaesackett">Kaelyn Sackett</a></h3>

<h3><strong>The Project</strong></h3>
<h5>RoomEase is a web application designed to make living with roommates easier by:</h5>
<ul>
  <li>Keeping track of your house's bills, and allowing you to see which bills you have and have not paid your share of.</li>
  <li>Allowing you to send messages to your roommates via the house message board.</li>
  <li>Providing a calendar where you can view all of the open bills for your house.</li>
  <li>Automatically sending text reminders to roommates that have unpaid bills with approaching due dates.</li>
</ul>

<h3><strong>Technologies Used</strong></h3>
RoomEase is written in Python 2.7, JavaScript, SQLite3, and HTML5/CSS3 with the uses of Flask, Bootstrap.js, Moment.js, Verify.js, jQuery, AJAX/JSON, Jinja2, and SQLAlchemy. Twilio API used for automated test message reminders, FullCalendar API used for calendar view.

<h3><strong>Environment</strong></h3>

1) Clone the repository:

<pre><code>$ git clone https://github.com/kaesackett/RoomEase.git</code></pre>

2) Create and activate a virtual environment in the same directory: 

<pre><code>$ pip install virtualenv
$ virtualenv env
$ source env/bin/activate 
</code></pre>

3) Install the required packages using pip:

<pre><code>(env)$ pip install -r requirements.txt
</code></pre>
