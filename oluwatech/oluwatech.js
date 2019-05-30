]\

exports.foo = 30
exports.you = 5999

var utils = {} 


utils.go = function() { 
    console.log("hiya there") 
}


utils.ts =  { 'get_in_car' : { 'reqs' : { 'a' : ['in_car' ]} , 
			       'mods' : { 'add' : ['in_car'],
					  'del' : ['at_!?'] }},
	      
	      'buy_food'   : { 'reqs' : { 'p'   : ['at_store' , 'have_money' ]},
			       'mods' : { 'add' : ['have_food'],
					  'del' : ['have_money'] }},
	      
	      'drive_to_bank' : { 'reqs' : {'p' : ['in_car'] } , 
				  'mods' : {'add' : ['at_bank'],
					    'del' : ['at_!?' , 'in_car'] }} , 
	      
	      'get_money' : {'reqs' : { 'p' : ['at_bank']} ,
			     'mods' : { 'add' : ['have_money']}},
	      
	      'drive_to_store' : {'reqs' :  {'p' : ['in_car']},
				  'mods' :  {'add' : ['at_store'],
					     'del' : ['at_!?' ,'in_car']}},
	      
	      'eat_food' : {'reqs' : {'p' : ['have_food']},
			    'mods' : {'add' : null , 
				      'del' : ['have_food', 'hungry']}} } 




utils.state =  [ "at-home", "hungry" ] 



utils.excludes = ["hungry"] 


exports.utils = utils


