"""
Prompts list for Pypercraft
"""

GENERATE_TITLE_PROMPT = """
        Generate an appropriate clever title for the paper concerning the following idea and topic:

        Idea: {idea}

        Topic: {topic}
        
        Make sure you use a {tone} tone in your writing style.

        Return the result as a single string, and do not mention the fact that this is a title or a paper.
        """

GENERATE_INTRODUCTION_PROMPT = """
        Generate an appropriate introduction for the paper concerning the following idea and topic:

        Idea: {idea}

        Topic: {topic}

        The length must be {num_words} words.
        
        Make sure you use a {tone} tone in your writing style.

        Return the result as a single string, and do not mention the fact that this is a introduction or a paper.
        """

GENERATE_BODY_PROMPT = """
        Current Introduction: {introduction}
        
        Using the previous introduction, generate appropriate body paragraphs for the paper 
        concerning the following idea and topic, but do not add a conclusion:

        Idea: {idea}

        Topic: {topic}

        The length of these paragraphs must be {num_words} words.
        
        Discuss the topic and idea extensively, to ensure you meet the word requirement of {num_words} words.
        
        Do not add or generate conclusion.
        
        Make sure you use a {tone} tone in your writing style.
        
        Return the result as a single string, and do not mention the fact that this is a body or a paper.
        """

GENERATE_CONCLUSION_PROMPT = """
        Generate an appropriate conclusion for the paper concerning the following idea and topic:

        Idea: {idea}

        Topic: {topic}

        The length must be {num_words} words.
        
        Make sure you use a {tone} tone in your writing style.

        Return the result as a single string, and do not mention the fact that this is a conclusion or a paper.
        """