from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.enums import TA_CENTER

from reportlab.lib.colors import darkblue

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.textColor = darkblue
title_style.alignment = TA_CENTER

heading = styles["Heading2"]

normal = styles["BodyText"]


def build_report(
        filename,
        ats,
        job,
        result,
        jd_result,
        roadmap,
        rewrite,
        career
):

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            "AI Resume Analyzer Report",
            title_style
        )
    )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {ats}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Job Match:</b> {job}%",
            normal
        )
    )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            "Professional Summary",
            heading
        )
    )

    story.append(
        Paragraph(
            result["summary"],
            normal
        )
    )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            "Strengths",
            heading
        )
    )

    for item in result["strengths"]:
        story.append(
            Paragraph(
                "• "+item,
                normal
            )
        )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            "Weaknesses",
            heading
        )
    )

    for item in result["weaknesses"]:
        story.append(
            Paragraph(
                "• "+item,
                normal
            )
        )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            "Missing Skills",
            heading
        )
    )

    for skill in result["missing_skills"]:
        story.append(
            Paragraph(
                "• "+skill,
                normal
            )
        )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            "Career Advice",
            heading
        )
    )

    story.append(
        Paragraph(
            career["career_summary"],
            normal
        )
    )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            "Learning Roadmap",
            heading
        )
    )

    for item in roadmap["roadmap"]:

        story.append(
            Paragraph(
                f"<b>{item['skill']}</b>",
                normal
            )
        )

        story.append(
            Paragraph(
                item["duration"],
                normal
            )
        )

        story.append(
            Spacer(1,8)
        )

    doc.build(story)