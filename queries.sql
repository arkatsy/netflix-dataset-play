-- How many directors are there in the dataset?
select count(distinct director)
from netflix_titles;

-- What director made the most movies & TV Shows?
select director, count(*) as total_movies
from netflix_titles
where director is not null
group by director
order by count(*) desc
limit(1);

-- What are the directors that made more than 5 movies?
select director, count(*) as total_movies
from netflix_titles
where director is not null
group by director
having count(*) > 5;


-- How many movies were made by each director?
select director, count(*) as total_movies
from netflix_titles
where director is not null and type = 'Movie'
group by director
order by count(*) desc;

-- Who are the directors that made both movies and TV shows?
select director
from netflix_titles
where director is not null
group by director
having count(distinct type) > 1;