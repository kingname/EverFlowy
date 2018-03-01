# EverFlowy

Sync your workflowy's items into evernote.

## Status

Now, by use the dev_token of evernote sandbox, I can sync the items of workflowy to evernote successfully:

![Example](http://7sbpmp.com1.z0.glb.clouddn.com/2018-02-25-16-15-23.png)

What I will do is enable it in the normal mode out of sandbox and use the Oauth2 get the access token of other
account.

Also, I will implement the `update function`. As you can see, I have already finished a module called SqlUtil, which
 is used to save the map of workflowy's item id and the notebook' GUID of evernote.
