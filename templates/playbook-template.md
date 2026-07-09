---
playbook_type: "standard"
name: "Your Playbook Name"
author: "your-github-username"
github_url: "https://github.com/your-username/your-repo"
description: "A one-line description of what this playbook automates."
license: "MIT"
tier: "unreviewed"
tags: ["tag1", "tag2"]
integrations: ["Tenable"]
agents_used:
  - name: "First Agent"
    role: "What this agent does in the chain"
    type: "exchange"
    ref: "slug-of-exchange-listing"
  - name: "Second Agent"
    role: "What this agent does in the chain"
    type: "github"
    ref: "https://github.com/user/repo"
  - name: "Manual Step"
    role: "Human review or decision point"
    type: "info"
date_added: 2026-01-01
---

Optional longer description of the playbook workflow.
The actual playbook content should remain in your GitHub repo.
