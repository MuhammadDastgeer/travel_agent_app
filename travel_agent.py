from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class TravelAgent:
    def __init__(self):
        # Get GROQ API key from environment variables
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            model="deepseek-r1-distill-llama-70b",
            temperature=0.7,
            groq_api_key=groq_api_key
        )
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=False
        )
        
        # Enhanced templates with more detailed prompts
        self.templates = {
            "city_info": """
            As a professional travel guide for {city}, provide comprehensive information including:
            1. Top 5-7 must-visit attractions with descriptions
            2. Best neighborhoods to explore
            3. Cultural highlights and local customs
            4. Ideal visit duration and seasonal considerations
            5. Safety tips and areas to avoid
            6. Public transportation overview
            7. Unique experiences only available in this city
            
            Present in clear sections with emoji icons for better readability.
            """,
            
            "hotels": """
            Recommend hotels in {city} categorized by:
            
            🏨 Luxury (5-star):
            - 2-3 options with premium amenities
            - Average nightly rates
            - Best features and guest reviews
            
            🛌 Mid-Range (3-4 star):
            - 3-4 best value options
            - Key amenities and location benefits
            
            🏠 Budget:
            - 2-3 clean, safe options
            - Hostels or budget hotels with good ratings
            
            For each category, include:
            - Proximity to attractions
            - Dining options
            - Transportation access
            - Special deals if available
            """,
            
            "distances": """
            Provide detailed travel information between {location1} and {location2} in {city}:
            
            🚶 Walking:
            - Distance: [x] km/miles
            - Time: [x] minutes
            - Route highlights
            
            🚕 Taxi/Rideshare:
            - Approximate cost
            - Time with normal traffic
            - Best taxi apps if applicable
            
            🚇 Public Transport:
            - Lines/routes to take
            - Fare information
            - Estimated time
            - Transfer points if any
            
            🚗 Driving:
            - Distance and time
            - Parking availability at destination
            - Toll roads if applicable
            
            Include any special tips for this route.
            """,
            
            "food": """
            Create a food guide for {city} with:
            
            🍽️ Iconic Dishes:
            - 5-7 must-try local specialties
            - Brief history of each dish
            - Where to find the best versions
            
            🏆 Top Restaurants:
            - Fine dining options
            - Best local eateries
            - Hidden gems known only to locals
            
            🍴 Dietary Considerations:
            - Vegetarian/vegan options
            - Halal/Kosher availability
            - Common allergens to watch for
            
            🛒 Food Markets:
            - Best markets for local food
            - What to buy there
            - Opening hours and tips
            
            Include any unique dining experiences like cooking classes or food tours.
            """
        }
    
    def get_city_info(self, city):
        prompt = ChatPromptTemplate.from_template(self.templates["city_info"])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"city": city})
    
    def get_hotels(self, city):
        prompt = ChatPromptTemplate.from_template(self.templates["hotels"])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"city": city})
    
    def get_distances(self, city, location1, location2):
        prompt = ChatPromptTemplate.from_template(self.templates["distances"])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "city": city,
            "location1": location1,
            "location2": location2
        })
    
    def get_food(self, city):
        prompt = ChatPromptTemplate.from_template(self.templates["food"])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"city": city})
    
    def general_conversation(self, query):
        return self.conversation.predict(input=query)