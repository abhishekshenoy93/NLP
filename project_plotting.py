import plotly.express as px
import plotly.graph_objects as go

def romcom_plot(new_list,scores_romcom, filename = None):
    ''' creating a bar plot for comedy, romance and romcom'''
    fig = px.bar( x= new_list, y=scores_romcom,
                 color=new_list,
                 height=400)
    
    # Creating layout for visuals
    fig.update_yaxes(range=[9.6,9.8]) # scaling the y axes to get better visuals

    fig.update_layout(
        title={'text':'Bar Plot of Romance Comedy and Both',
              'xanchor':'center', 'yanchor':'top', 'x':0.5},
        xaxis_title="Genres",
        yaxis_title="Average_sentiment",
        legend_title="Genre",
        font=dict(
            size=15,
            color="Black"
        )
    )
    
     # File Name String and storing as html 
    if filename != None:
        fig.write_html(f'{filename}.html')


    return fig.show()


def sum_genre_plot(df2,filename = None):
    ''' creating a bar plot for getting sum of each genres to visualize'''
    fig = px.bar(df2, x='genres', y='total',
                 hover_data=['genres', 'total'], color='genres',
                  labels={'total':'sum of genres'},height=400)
    
    # Creating layout for visuals
    fig.update_layout(title={'text':'Sum Of Each Genres',
                      'xanchor':'center', 'yanchor':'top', 'x':0.5},
                     bargap = 0.5,
                     height = 600,
                     width =1600,
                     xaxis_title="Genres",
                     yaxis_title="Sum of Genres",
                     legend_title="Genres",
                     font=dict(
                     size=15,
                     color="Black"
                        )
                     )
    
     # File Name String and storing as html 
    if filename != None:
        fig.write_html(f'{filename}.html')
    return fig.show()
 
def side_by_side_sentiment_vs_imdb_rating_by_genre(my_columns,sentiment_scores,imdb_scores, filename = None):
    ''' creating a scatter plot to visualize and interact genres with Average Imdb Rating W.R.T Average Sentiment Score'''
    fig = go.Figure()
    the_list = my_columns
    fig.add_trace(go.Bar(
      x = the_list ,
      y = sentiment_scores,
      name = "review_sentiment",
    ))

    fig.add_trace(go.Bar(
      x = my_columns,
      y = imdb_scores,
      name = "imdb_rating",
    ))
    
    # Creating layout for visuals
    fig.update_layout(title={'text':'Genre Average Sentiment Score w.r.t Imdb Rating',
                      'xanchor':'center', 'yanchor':'top', 'x':0.5},
                     bargap = 0.5,
                     height = 600,
                     width =1600,
                     xaxis_title="Genres",
                     yaxis_title="Average Sentiment & Imdb Rating",
                     legend_title="Ratings",
                     font=dict(
                     size=15,
                     color="Black"
                        )
                     )

    fig.update_yaxes(range=[8.0,10]) # scaling the y axes to get better visuals
    fig.update_xaxes(tickangle = -45) # cretaing the labels on x axes at -45 degrees
    
     # File Name String and storing as html 
    if filename != None:
        fig.write_html(f'{filename}.html')
    
    return fig.show()

def avg_sentiment_by_genre_plot(my_columns,sentiment_scores, filename = None):
    ''' creating plot for genres with average sentiment scores from reviews'''
    fig = px.bar( x= my_columns, y=sentiment_scores,
                  color=my_columns,
                  height=400)
    fig.update_yaxes(range=[9.6,9.8]) # scaling the y axes to get better visuals
    
    # Creating layout for visuals
    fig.update_layout(title={'text':'Avearge Sentiment By Genre',
                      'xanchor':'center', 'yanchor':'top', 'x':0.5},
                     bargap = 0.5,
                     height = 600,
                     width =1600,
                     xaxis_title="Genres",
                     yaxis_title="Average Sentiment",
                     legend_title="Genres",
                     font=dict(
                     size=15,
                     color="Black"
                        )
                     )
    
     # File Name String and storing as html 
    if filename != None:
        fig.write_html(f'{filename}.html')
    return fig.show()

def movie_scatter_plot(df, filename = None):
    ''' creating plot for getting all movie title and comparing it with imdb reviews and average sentiment scores'''
    fig = px.scatter(df, x="weighted_sentiment",y="movie_title", color="rating")
    fig.update_traces(marker_size=5)
    fig.update_xaxes(range=[8.85,10]) # scaling the x axes to get better visuals
    
    # Creating layout for visuals
    fig.update_layout(title={'text':'Movies with Imdb Rating and Average Sentiment',
                      'xanchor':'center', 'yanchor':'top', 'x':0.5},
                     bargap = 0.5,
                     height = 600,
                     width =1600,
                     xaxis_title="Average Sentiment Score",
                     yaxis_title="Movies",
                     legend_title="Imdb Rating",
                     font=dict(
                     size=15,
                     color="Black"
                        )
                     )
    # File Name String and storing as html 
    if filename != None:
        fig.write_html(f'{filename}.html')
    return fig.show()