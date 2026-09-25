# Context

A support engineer noticed something odd while testing with a
non-admin test account:

> The "Delete user" button doesn't show up for me in the admin panel
> since I'm not an admin, but I was poking around with the browser dev
> tools and noticed the network request it sends is just a normal DELETE
> to `/api/users/:id`. Out of curiosity I replayed that exact request from
> my own (non-admin) session with a different user's id, and it worked --
> the user got deleted. Is the button hiding the only thing stopping a
> non-admin from doing this?

Files in this directory are the complete evidence available about this
system -- there is nothing else to consult.
