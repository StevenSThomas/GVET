# GVET - Getty Vocabulary Explorer Tool

## Features

- a user is uniquely identified and can log into to the application
- a user can search the Art & Architecture Thesaurus by term and/or note using AND, OR, exact match with "" and right truncation wildcard with -
- a user can browse the ATT hierarchies
- a user can view a subject detail (might need to be able to compare multiple subjects)
- a user can maintain personal lists of ATT subjects
- a user can view recently revised subjects, the following filters are available
	- edits
	- adds, delete, or modified terms
	- scope note edits
	- moved records
	- new records
	- all edits and record types
	- deleted records

## Getty Vocabularies




## Decisions

- call getty API directly from javascript, or introduce my own backend that transforms the getty API into my own interface
	- create my own backend to demonstrate my abilities in both front end and backend
	- add additional capabilities like current user, saved items, recent searches
- use server rendered html or a front end framework
- for front end, use a component framework or build by own components
	- use a component framework to save time
	- which component framework
		- choose PrimeVue due to minimalism, easy to theme, contained the types of components I need and looked simple to pickup
- project layout
    - seperate domain logic from web server functionality

## Constraints

- ~8 hours of development time
- include front end and use vue.js because it is listed as the chosen front end framework on the job description
- use flask as backend because it is listed as the chosen backend framework
- use getty vocabulary APIs

## Code Organization

