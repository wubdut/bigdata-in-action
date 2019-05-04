select t.site_id, t.total_click/t.total_show as ctr 
    from ( 
	  select site_id, sum(click) as total_click, count(*) as total_show 
	  from ctr_data 
	  group by site_id
    ) t 
order by ctr limit 10;  
