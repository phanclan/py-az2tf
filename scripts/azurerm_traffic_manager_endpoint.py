def azurerm_traffic_manager_endpoint(crf,cde,crg,headers,requests,sub,json,az2tfmess,azr):
    #  125 traffic manager endpoint

    tfp="azurerm_traffic_manager_endpoint"

    if crf in tfp:
    # REST or cli
    # from above
        
        tfrmf="125-"+tfp+"-staterm.sh"
        tfimf="125-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            #loc=azr[i]["location"]
            id=azr[i]["id"]
            pname=azr[i]["name"]
            azr2=azr[i]["properties"]["endpoints"]
            jcount=len(azr2)
            print "jcount=" + str(jcount)
            for j in range (0,jcount):

                name=azr2[j]["name"]
                id=azr2[j]["id"]
                rg=id.split("/")[4].replace(".","-")
                rgs=id.split("/")[4]
                print rg
                print crg
                if crg is not None:
                    if rg.lower() != crg.lower():
                        continue  # back to for
                
                rname=name.replace(".","-")
                prefix=tfp+"."+rg+'__'+rname
                print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                #fr.write('\t location = "'+ loc + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')
                fr.write('\t profile_name = "' +  pname + '"\n')
                ttype=azr2[j]["type"].split("/")[2]
                fr.write('\t type = "' +  ttype + '"\n')
                print "hi2"
                pri=azr2[j]["properties"]["priority"]
                fr.write('\t priority = "' +  str(pri) + '"\n')
                wt=azr2[j]["properties"]["weight"]
                fr.write('\t weight = "' +  str(wt) + '"\n')

                tgt=azr2[j]["properties"]["target"]
                fr.write('\t target = "' +  tgt + '"\n')
                eps=azr2[j]["properties"]["endpointStatus"]
                fr.write('\t endpoint_status = "' +  eps + '"\n')
                try:
                    #tgtid=azr2[j]["properties"]["targetResourceId"]
                    tgtrrg=azr2[j]["properties"]["targetResourceId"].split("/")[4].replace(".","-")
                    tgtrid=azr2[j]["properties"]["targetResourceId"].split("/")[8].replace(".","-")          
                    fr.write('\t target_resource_id = "${azurerm_public_ip.' + tgtrrg + '__' + tgtrid + '.id}"\n')
                except KeyError:
                    pass


                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print f.read()

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  
            # end for j loop

        # end for i loop

        tfrm.close()
        tfim.close()
    #end traffic manager endpoint