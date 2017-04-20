int * compute_prefix(string p)
{
	int m=p.length();
	int *pi=(int *)(malloc((m)*sizeof(int)));
	pi[0]=0;
	int k=0;
	for (int i = 1; i < m; ++i)
	{
		while(k>0 && p.at(k)!=p.at(i))
		{
			k=pi[k-1];
		}
		if(p.at(k)==p.at(i))
		{
			k=k+1;
		}
		pi[i]=k;
	}
	return pi;
}

vector<int> kmp(string t,string p,int start,int end)
{
	vector<int> occurs;
	int m=p.length();
	int *pi=(int *)(malloc((m)*sizeof(int)));
	pi=compute_prefix(p);
	int q=0;
	for (int i = start; i <end; ++i)
	{
		while(q>0 && p.at(q)!=t.at(i))
		{
			q=pi[q-1];
		}
		if(p.at(q)==t.at(i))
		{
			q=q+1;
		}
		if(q==m)
		{
			occurs.push_back(i-(m-1));
			q=pi[q-1];
		}
		
	}
	free(pi);
	if(occurs.size()>0)
	{
		return occurs;
	}
	else
	{
		occurs.push_back(-1);
		return occurs;
	}
	
}
