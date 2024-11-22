Description


I wanted to briefly explain the choices I made regarding the data visualization and data handling in my project:
1.	Handling Large Dataset: The dataset I’m working with is quite large, which caused issues when trying to load it all at once, sometimes resulting in errors. To mitigate this, I split the data into smaller parts, saving each as a separate CSV file. This approach allows me to load the data in manageable chunks, making the process more efficient and avoiding system overload.

2.	Melting the Dataframe for Better Structure: To effectively analyze and visualize the data, I melted the dataframe to extract the different energy sources, units, and types of energy. This transformation allowed me to reshape the data in a more structured format, making it easier to work with and plot for various energy sources.

3.	Bar Chart vs. Pie Chart: Initially, I considered using a pie chart to visualize the distribution of energy sources. However, I encountered an issue with overlapping labels, making it difficult to interpret the chart clearly. To address this, I opted for a bar chart instead. The bar chart offers better clarity and allows the labels to remain legible without overlap, providing a more effective way to show the distribution of the data.

