# 👋 NEI-ISEP Informatics

Welcome to the Informatics Department of the **Núcleo de Estudantes de Informática do ISEP (NEI-ISEP)**.

We develop and maintain the digital platforms used by students and by the organization, build websites and tooling for NEI events, and support the infrastructure required for the department's day-to-day operation.

## 🎯 Mission

Our mission is to make NEI's software and infrastructure reliable, secure and maintainable while giving students a place to build real products and learn modern engineering practices.

We work across web applications, APIs, authentication, databases, CI/CD, containers, observability and organization infrastructure.

## 💻 Platforms

### 📚 Antirecurso

[Antirecurso](https://github.com/Nucleo-Estudantes-Informatica-ISEP/antirecurso) is the student resource platform for sharing and accessing course material, exams, notes, questions, scores and related academic workflows.

The current backend is the [AdonisJS Antirecurso API](https://github.com/Nucleo-Estudantes-Informatica-ISEP/antirecurso-api-adonis).

### 🔄 Unclassed

[Unclassed](https://github.com/Nucleo-Estudantes-Informatica-ISEP/unclassed) helps ISEP Informatics students manage class and subject swap requests, including automated matching and notification workflows.

### 🛰️ Orbit

[Orbit](https://github.com/Nucleo-Estudantes-Informatica-ISEP/orbit) is NEI's internal operations platform for members, departments, projects, tasks, recruitment, inventory, events, plans and other organization workflows.

### ⚡ NEI Website

The [NEI website](https://github.com/Nucleo-Estudantes-Informatica-ISEP/nei-website) is the public home of the organization, its departments, activities and useful information for students.

## 🎪 Events

### 👨🏻‍💻 FallStack

[FallStack](https://github.com/Nucleo-Estudantes-Informatica-ISEP/fallstack-website) connects ISEP students with companies, internships and career opportunities through talks, stands and networking activities.

Visit the latest event at [fallstack.nei-isep.org](https://fallstack.nei-isep.org/).

### 👾 Game Jam

NEI Game Jam is an intensive game-development event where students build and present games in a hackathon-style format.

Visit [gamejam.nei-isep.org](https://gamejam.nei-isep.org/) for the latest edition.

### 🌱 CodeSpring

CodeSpring is another recurring NEI technology event. Repositories for an edition may remain private while the event is being prepared and can be published after partner/private information has been reviewed.

## 🔐 Repository policy

We keep repositories private while they contain unreleased event information, partner details, credentials or other material that must not be public. Maintained software projects should be made public once a security/privacy review is complete when there is no operational reason to keep the source private.

Existing project licenses are preserved. A public repository with no license remains under default copyright rules unless the project maintainers deliberately choose a license.

## 🛠️ Engineering standards

Shared contribution policy, security guidance, release automation, secret scanning and repository standards live in the organization's [`.github` repository](https://github.com/Nucleo-Estudantes-Informatica-ISEP/.github).

Runtime-changing pull requests to `main` in participating projects use semantic release labels (`release:patch`, `release:minor`, `release:major`). Dependabot and documentation/CI/metadata-only changes do not create application releases.

Project-specific build, test, migration and deployment checks remain inside each repository so changing a framework or package manager in one application does not break unrelated projects.

## 📞 Contact us

For Informatics Department questions, collaboration or operational support:

**Email:** [informatica@nei-isep.org](mailto:informatica@nei-isep.org)

For suspected vulnerabilities, do not open a public issue; follow the organization or repository-specific `SECURITY.md` policy.
