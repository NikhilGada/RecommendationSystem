Recommender systems are one of the most successful and widespread applications of machine learning technologies in business. You can find large-scale recommender systems in retail, video on demand, or music streaming services. In order to develop and maintain such systems, a company typically needs a group of experienced data scientists and engineers.
The first one is about human nature. Our memory is not perfect, we tend to forget things. If early in the morning we made a list of goods to buy for dinner, we can lose the list during the day, and there will be something we won't be able to recall.
Business is successful when it is beneficial for clients and solves their problems. Recommendations simplify daily shopping and help to not overlook something. That's why customers are happy and willing to pay for what they really need.
How recommendations boost retail
Help to understand what customers really need
Personal approach increases customers' loyalty by saving their time
Motivate people to buy more
You can create demand for new products by adding them to suggestions

There are three major components of the Apriori algorithm:
Support
Confidence
Lift
Support
Support is basically tells how popular is the item. Support is calculated by the no of order or transactions having the product B out of total no of order.

Confidence
Confidence refers to the likelihood that an item B is also bought if item A is bought. It can be calculated by finding the number of transactions where A and B are bought together, divided by total number of transactions where A is bought. Mathematically, it can be represented as:

Lift
Lift(A,B) refers to the increase in the ratio of sale of B when A is sold. Lift(A,B) can be calculated by dividing Confidence(A,B) divided by Support(B). Mathematically it can be represented as:

You can draw some conclusion by seeing lift value. Lift value 1 tells that there is no association between the products. Lift value greater than 1 means the products are likely to bought together. Lets say lift value is coming as 5 for two product A and B. This means product A and B are 5 times more likely to bought together than just buying product B alone. A lift value less than 1 suggest that products are unlikely to bought together.
