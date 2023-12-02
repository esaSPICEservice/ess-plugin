#include <string>
#include <stdio.h>
#include <dlfcn.h>
 
int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("Scenario root path needed\n");
        return -1;
    }
   
    std::string librarypath = "./libosve-if.so";
    void *libhandle = dlopen(librarypath.c_str(), RTLD_LAZY | RTLD_DEEPBIND); //functions loaded

    if (libhandle == NULL) {
        perror("dlopen failure");
    }

    typedef int(*osve_executeFunc)(const char *, const char *);
    osve_executeFunc osve_execute = (osve_executeFunc) dlsym(libhandle, "osve_execute");

    if (osve_execute == NULL) {
        perror("osve_execute failure");
        return 0;
    }

    std::string scenarioPath =  argv[1];
    std::string sessionFilePath =  scenarioPath + "/session_file.json";

    int result = osve_execute(scenarioPath.data(), sessionFilePath.data());

    dlclose(libhandle);

    return result;
}