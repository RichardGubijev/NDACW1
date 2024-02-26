# Ideas

## Question 1
> If both editors have been commenting more than usual on the same day <br>
> how plausible it is that this behaviour has not propagated yet to neighbouring similar editors?

Commenting more = amount of degrees
- Check the mean and median and do calculations 
- suspicious if current nodes degree > median/mean 

Measure of similarity = edge intersection between the current node and each of the neighbours <br>
Ex. <br>
current node neighbours = [A,B,C,D,E] <br>
neigh A = [B,F,Q,W]      -> similarity = 1/5 <br>
neigh B = [A,E,D,X,Y,Z]  -> similarity = 3/5 <br>

The calculation will be (current node neighbours & neigh #)/len(current node neighbours)


## Question 2
> if the editor has “possibly trolling” -> check other editors <br> 
> prioritise those with a higher chance of trolling. <br>
> priority list on what editors to check first?

Median = 1, mean = 6

current_node_1 has degree 1
current_node_2 has degree 20



we check for current_node_2 as this is the suspicious one

current_node_2 has 18 neighbours with degree 1, let's look at the other two, let's call them A and B

node A 
- 50 degree
- similarity of 100%

node B 
- 150 degree
- similarity of 50%

priority queue option 1 = [A, B, ...]  where we use similarity as a measure <br>
priority queue option 2 = [B, A, ...]  where we use degree as the measure <br>
priority queue option 3 = [B, A, ...]  where we use overlap*degree as the measure <br>