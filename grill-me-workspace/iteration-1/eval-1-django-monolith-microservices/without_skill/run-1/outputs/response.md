# Baseline Response (no skill): Django Monolith to Microservices

Okay, let's get into it — because I have a lot of questions, and honestly, some concerns.

**The number 8 worries me right away.** Where did 8 come from? Did you map your domain boundaries first and land on 8 naturally, or did someone draw boxes on a whiteboard and count them? "8 microservices" sounds like a target that was chosen before the analysis was done. How confident are you that your domain actually has 8 clean seams — and not 5, or 12, or 3?

**200k LOC in 6 months with 5 devs is extremely aggressive.** That's not a refactor — that's a full architectural replacement while presumably still shipping features and keeping the lights on. Have you actually modeled what percentage of dev capacity this migration will consume? If it's more than 40-50%, you're probably already behind on your roadmap before you start.

**How coupled is your data?** Django monoliths almost always have a single database with cross-model foreign keys everywhere. The hardest part of microservices isn't splitting the code — it's splitting the data. Have you done a dependency graph of your models? Do you know which services will own which tables, and what happens to the joins that currently span those boundaries? If you haven't answered that question in detail, you don't actually have a plan yet — you have an intention.

**What's your inter-service communication strategy?** Synchronous REST/gRPC between services, async messaging (Kafka, RabbitMQ, Celery?), or some mix? How are you handling distributed transactions? Django's ORM gives you atomic transactions basically for free — once you split the data, you lose that. Have you thought through what happens when service B fails mid-operation that service A already committed?

**Do you have the operational maturity for this?** Microservices require serious infrastructure investment: service discovery, distributed tracing, centralized logging, health checks, independent CI/CD pipelines, container orchestration. With 5 devs, who is owning that? Is it already in place, or are you building it as you go? If it's not already in place, add 2-3 months to your estimate.

**What's actually driving this?** Scaling bottlenecks? Team autonomy? Resume-driven development? The answer matters a lot. If it's "we need to scale the payments module independently," there might be a much cheaper solution. If it's "our deploy takes 45 minutes and blocks everyone," that's more legitimate — but even then, a modular monolith might get you 80% of the benefit for 20% of the cost and risk.

**What's your rollback plan if you're 4 months in and it's not working?** This is the question most teams can't answer, and it's the one that tells you the most about how much real planning has happened.

The teams that succeed at this kind of migration go in knowing exactly which service they're extracting first (usually the one with the cleanest boundary and lowest coupling), run it as a strangler fig pattern alongside the monolith, and don't commit to a hard date for "all 8 done." The ones who fail usually picked a date, a number, and a team size — and skipped the dependency analysis.

So: walk me through the domain boundaries you've identified. How did you decide what goes in each service, and which one are you planning to extract first?
