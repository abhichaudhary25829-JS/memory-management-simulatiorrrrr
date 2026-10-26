import plotly.graph_objects as go
import plotly.express as px

def line_chart(rows, fields, title=""):
    fig=go.Figure()
    for field in fields: fig.add_trace(go.Scatter(x=list(range(1,len(rows)+1)),y=[r.get(field) for r in rows],mode="lines+markers",name=field))
    fig.update_layout(title=title,template="plotly_dark",height=310,margin=dict(l=10,r=10,t=45,b=10),paper_bgcolor="#101827",plot_bgcolor="#101827")
    return fig

def bar(data,x,y,title=""):
    fig=px.bar(data,x=x,y=y,template="plotly_dark",title=title,color_discrete_sequence=["#25c7d9"])
    fig.update_layout(height=310,margin=dict(l=10,r=10,t=45,b=10),paper_bgcolor="#101827",plot_bgcolor="#101827")
    return fig
