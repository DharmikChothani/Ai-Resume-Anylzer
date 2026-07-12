import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def ats_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,

            title={"text":"ATS Score"},

            gauge={
                "axis":{"range":[0,100]},

                "bar":{"color":"green"},

                "steps":[

                    {"range":[0,40],"color":"red"},

                    {"range":[40,70],"color":"orange"},

                    {"range":[70,100],"color":"lightgreen"}

                ]
            }
        )
    )

    return fig

def job_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,

            title={"text":"Job Match"},

            gauge={
                "axis":{"range":[0,100]}
            }
        )
    )

    return fig



def skill_chart(skills):

    df=pd.DataFrame({

        "Skill":skills,

        "Score":[100]*len(skills)

    })

    fig=px.bar(

        df,

        x="Skill",

        y="Score"

    )

    return fig
def resume_scores():

    df=pd.DataFrame({

        "Section":[

            "Summary",
            "Projects",
            "Skills",
            "Experience"

        ],

        "Score":[

            80,
            92,
            75,
            88

        ]

    })

    fig=px.bar(

        df,

        x="Section",

        y="Score"

    )

    return fig
def radar():

    categories=[

        "Python",
        "SQL",
        "ML",
        "Docker",
        "AWS"

    ]

    values=[

        95,
        80,
        88,
        30,
        20

    ]

    fig=go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=values,

            theta=categories,

            fill="toself"

        )

    )

    return fig