# Create a scatter plot of Age vs Salary using ggplot2
ggplot(data, aes(x = Age, y = Salary, label = Name)) + 
  geom_point(size = 3, color = "blue") +  # Add blue points to the plot
  geom_text(vjust = -0.5, hjust = 0.5, color = "black") +  # Add text labels just above the points
  labs(title = "Age vs Salary", x = "Age", y = "Salary") +  # Set the title and axis labels
  theme_minimal()  # Apply a minimal theme for a clean look
