# Part 2: Research (30 Points)  

Useful: refetchQueries, setQueryData, enabled  
Advanced: Optimistic Updates  

### refetchQueries  
What does it do? Explain the feature in your own words.  
=> It's a method belonging to QueryClient. It triggers a re-run fetch for all entries that match a filter, regardless if that data is considered stale or not.  

Why would someone use it? Describe a realistic situation where it would be helpful.  
=> Pretty much forcing an update. Maybe there's a "refresh" button that the user can manually click to trigger a re-fetch, even if it was last updated 5 seconds ago and the staleTime is larger than that.  

How does it work? Provide a small example of the relevant code and explain the important parts.  
```
function RefreshButton() {
  const queryClient = useQueryClient()

  const handleRefresh = async () => {
    await queryClient.refetchQueries({ queryKey: ['orders'] })
    console.log('Orders are up to date')
  }

  return <button onClick={handleRefresh}>Refresh</button>
}
```
    If we only had a const {data, ...otherstuff} = useQuery(), the fetching would be on an interval based on staleTime. .refetchQueries() allows us to fetch anything with a matching key on manual trigger. Here, it'll look at the key 'orders' in cache and re-fetch all of it.  

### setQueryData  
What does it do? Explain the feature in your own words.  
=> It's a method belonging to queryClient. It basically sets a specific cached entry directly. Like calling [key] = value on a dictionary. This doesn't make any network calls inherently.

Why would someone use it? Describe a realistic situation where it would be helpful.  
=> Say a PUT request is sent to edit a to-do item in a tasks management app. Typically, PUT requests return the updated item upon success. setQueryData() can be used to directly updating the cache without making a network request  

How does it work? Provide a small example of the relevant code and explain the important parts.  
```
setQueryData(queryKey, (oldData) => newData)
```
=> I thought this was enough to communicate. When you call this, it will update the cached data like [queryKey] = newData. That is, the cache that corresponds to the specific key ```queryKey``` will now have the value of ```newData```. Will not throw KeyNotFound; it will just makea a new query entry.    
    If ```newData``` is undefined, though, the data will not be updated.  
In context:  
```
function useUpdateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (updatedUser) =>
      fetch(`/api/users/${updatedUser.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedUser),
      }).then((res) => res.json()),

    onSuccess: (savedUser) => {
      queryClient.setQueryData(['user', savedUser.id], savedUser)
    },
  })
}
```
    Here, we can call useUpdateUser() to... update a user. useMutation is here to TRIGGER an effect-ful operation (POST/PUT/PATCH/DELETE). When mutationFn gets called and resolves, the resolved object is what mutationFn returns & onSuccess retrieves data from it (here as ```savedUser```). Then yeah it. Updates. Instead of having to do a GET to retrieve that item, Tanstack supports saving it within the same flow.  

### enabled  
What does it do? Explain the feature in your own words.  
=> another option for useQuery(). It controls when a fetch/the queryFn can run.  

Why would someone use it? Describe a realistic situation where it would be helpful.  
=> It's especially useful for queries that depend on some condition to not break. For example, you may have an app that lets each user have their own list of projects. Fetching projects will be an issue if the user isn't logged in yet, so the identifying item (ID) would be undefined. Or something more minute like length of an input box    

How does it work? Provide a small example of the relevant code and explain the important parts.  
```

function Projects({ email }) {
  const { data: user } = useQuery({
    queryKey: ['user', email],
    queryFn: () => fetchUserByEmail(email),
  })

  const userId = user?.id

  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects', userId],
    queryFn: () => fetchProjects(userId),
    enabled: !!userId,
  })

  if (!userId) return <p>Loading user...</p>
  if (isLoading) return <p>Loading projects...</p>
  return <ul>{projects.map((p) => <li key={p.id}>{p.name}</li>)}</ul>
}
```
    Query #2 is where we use enabled here. This is because we'd only want to fetch projects if there is a userId. (The !! operator extracts whether it's truthy or falsy into a boolean)  

### Optimistic Updates    
What does it do? Explain the feature in your own words.  
=> It updates the UI as if the request was successful; it's "optimistic" about its assumption. If the request turns out to fail, the UI rolls back to the previous state.  

Why would someone use it? Describe a realistic situation where it would be helpful.  
=> It helps the application feel more instant. Say you have a to-do app (you always have a to-do app). The app will feel sluggish because every "Mark Complete" waits on the server confirming it passed. Optimistic Updates would have the UI check out the checkbox right away, before the request even finishes on the server side / makes it back.  
=> It's especially good for requests that almost always succeeds.  

How does it work? Provide a small example of the relevant code and explain the important parts.  
```
function useToggleTodo() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: // callback fn

    onMutate: async (todo) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] })

      const previousTodos = queryClient.getQueryData(['todos'])

      queryClient.setQueryData(['todos'], (old) =>
        old.map((t) => (t.id === todo.id ? { ...t, done: !t.done } : t))
      )

      return { previousTodos }
    },

    onError: (err, todo, context) => {
      queryClient.setQueryData(['todos'], context.previousTodos)
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })
}
```
    The documentation says there are 2 ways to do it: onMutate (cache-based; update the cache directly) OR using the returned variables from useMutation() to update the UI  
    The example is the cache-based approach. When onMutate is triggered, we clear queries from overwriting our assumed optimistic updates (.cancelQueries) and saves current cache in case we need to roll back (previousTodos).  
    Then we manually update the cache ourselves via .setQueryData. That's the optimistic update part.  
    Aftermath: if it fails, roll it back (previousTodos).  
    Cleanup: either way, we sync with the server's real data when this all finishes (.invalidateQueries). I believe this isn't inherently necessary to "make it work," but it prevents wrong data.  

# Part 3: Comparison and Reflection (10 Points)  
1. Which of the four features you researched would be most useful in an application you've already built? Explain why.  
=> Optimistic Updates. I can see it in pretty much any use case that *does* need to make a request, but it's minute enough that it almost always succeeds. Plenty of to-do apps have been made, so this applies. IF my final project from the past was in React && I want to re-visit it, I could see myself using it for message reactions (we did a messaging app), for example.  

2. Which feature was the most difficult to understand? What made it confusing?  
=> None of them beat the others in difficulty by a significant margin. But probably Optimistic Updates. Mostly because it's not a dedicated object/method, but rather a synthesized usage of multiple methods to make it work. There's just more moving parts, so figuring out "is this part necessary or is it there for long-term stability" level of complexity is there, which is not present in the other single-part features.  

3. Of the advanced features, which would you most like to experiment with in a future project? Why?
=> Optimistic updates is already great. I do want to look more into Infinite Quries and Custom query/mutation hooks. The first is because: even the Pokemon app would want it! But also, learning a core feature in social media scrolling app would be useful. Profitable to make more apps that capitalize off people's dopamine. The latter choice is because I don't fully get what it'd be for.  

 

