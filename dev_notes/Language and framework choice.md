**Author: Szymon Gałecki**
### Language choice - Python
1. **Everyone in our team knows Python.** Code review can be done by anyone, we do not spend time on learning a new language and it is easier to stay in the loop.
2. **Short development time.** Python is great for prototyping and producing MVP in short time. The goal was to have a running solution as fast as possible and apply changes on the way. 
3. **Python is popular.** There are tons of packages, tutorials and SO posts. When creating something for the first time it is generally easier to do it in a way that was tested by many people who have documented their process.

### Application framework choice - Django
1. Django is the most mainstream framework to create web applications in Python.
2. It has built-in security features against SQL injections and cross-site scripting.

### API framework choice - FastAPI
1. FastAPI is easy to use, intuitive, and performative framework to build APIs in Python.
2. Why not Django rest framework? Application and API were created in the same time frame by two different people. To eliminate development dependency we built two separate solutions so that we could deliver faster.