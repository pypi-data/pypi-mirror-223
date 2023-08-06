# SymphonyMarkdown

A component to render HTML from markdown files.
The provided markdown can be edited within the component.
For example, displaying information about a particular analysis:

```
report.widget(SymphonyMarkdown,
    page="Overview",
    width="M",
    content=open("README.md").read()
)
```
