# Design Document

## Technical Decisions
### In this section, share and justify the technical decisions you made.
You don't need to respond to all questions, but you might find some of the following helpful:
* What design challenge(s) did you run into while completing your project? How did you choose to address them and why?

The majority of our design challenges fell into the creation and especially implementation of the matching algorithm. To provide a little context, our app is primarily to match people based on their classical music preferences so after taking a ten question quiz, the users are provided a score between 0 and 100 that displays their compatibility with every other user. In order to do so, we had to create an algorithm that would initially sort the users based on their answers and then find how similar they were to each other. At first we struggled to find a not very complicated way of sorting the users in a way that would allow for us to then find similarities between them. Eventually, we realized that we could create a coordinate system in four dimensions to which an answer would add to one dimension. In our code, to keep it simple, answering a for any question would add to the x axis or dimension. Then each user’s final “score” from the quiz would be a point in a euclidean space. This allowed us to find relative similarities between the users by finding the distances between every point then normalizing to have the values fall between 0 and 100. Next, we ran into problems with the implementation of this algorithm, especially with accessing and indexing our SQL database and using Flask. This simply required a lengthy process of debugging and iteration that eventually led to the app working. 

* Was there a feature in your project you could have implemented in multiple ways? Which way did you choose, and why?

As aforementioned, there were many ways in which we could have implemented the sorting and matching algorithms. For example, we were strongly considering using a T test to find correlations between various users but struggled to come up with how to assign them initially to categories. We eventually stuck with using a coordinate system in four dimensional euclidean space because it was very intuitive and allowed for us to potentially expand the numbers of categories as a function of angles around the axes. 

* If you used a new technology, what did you learn about this new technology? Did this technology prove to be the right tool?

We did not use any new technology but rather expanded on what could be done using the knowledge from previous psets, especially Finance. 

## Ethical Decisions
### What motivated you to complete this project? What features did you want to create and why?

With so many new dating apps coming out every month at Harvard, each one targeting different or maybe even the same audiences, we wanted to make a very niche app that would match people based on their classical musical preferences. Initially, we were intent on making this a dating app but quickly realized that there was no point especially to categorize people based on their sexual preferences as well as identities. This was one of the ethical dilemmas we faced as we realized that it would be quite tricky as well as technically difficult to account for not only cis heterosexual individuals but every identity. 

Our main focus for this project was to create a working and reliable algorithm that would match people based on their preferences and we successfully made such an algorithm. It can definitely still be improved but it is set up in a way so that the base idea would stay the same and how the information is processed would differ based on the number of categories considered or even how the questions are weighted. We also made a musicians page that displayed each person with their contact information and compatibility scores in order to connect users.

### Who are the intended users of your project? What do they want, need, or value?
You should consider your project's users to be those who interact _directly_ with your project, as well as those who might interact with it _indirectly_, through others' use of your project.

The intended audience and direct users are classical musicians or classical music lovers who are interested in connecting with other people with similar music interests. As classical musicians ourselves, we value taste in music and consider it to be not necessarily an important factor when making connections, but something quite interesting to discuss. We have always found that music is a great way to build connections as something to build off from, whether that be through disagreement or agreement when considering what music is subjectively good. This is another reason why we do not just list the top compatibility scores but also the lowest because in some ways that is another reason to connect with someone. The indirect users of the platform would be those such as classical musicians or lovers who are introduced mutually through users of the platform or even family members of the users. This app is intended for individuals to use so the indirect users are limited to people close to the direct users. 

### How does your project's impact on users change as the project scales up? 
You might choose one of the following questions to reflect on:
* How could one of your project's features be misused?
* Are there any types of users who might have difficulty using your project?
* If your project becomes widely adopted, are there social concerns you might anticipate?

In the current state of the project, every user’s email address is accessible to everyone which is definitely a concern as the project scales. This is somewhat a breach of privacy as then any user can maliciously gain access to other people’s personal information without even having asked for their permission. Furthermore, the quizzes are not accurately representative of someone’s musical taste and especially of that person’s compatibility with another user. The website is an extreme simplification of how to match and sort people based on their music preferences, especially since it only has ten very simple questions and only four categories into which people are sorted. Also, each question can only increase the score of a user in one dimension, meaning an answer does not weigh into more than one category when perhaps sometimes it should as answers can be nuanced. 
