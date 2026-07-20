# Changelog - flexible-v2.1

## Updated (adição de disciplina)

### edo:Hook (line 7139)

```diff
-         edo:hasDiscipline edo:SubseaRigidPipesEngineering ;
+         edo:hasDiscipline edo:SubseaRigidPipesEngineering ,
+                           edo:SubseaFlexiblePipesEngineering ;
```

### edo:KenterLink (line 8711)

```diff
-               edo:hasDiscipline edo:SubseaRigidPipesEngineering ;
+               edo:hasDiscipline edo:SubseaRigidPipesEngineering ,
+                                 edo:SubseaFlexiblePipesEngineering ;
```

### edo:PearLink (line 13973)

```diff
-             edo:hasDiscipline edo:SubseaRigidPipesEngineering ;
+             edo:hasDiscipline edo:SubseaRigidPipesEngineering ,
+                               edo:SubseaFlexiblePipesEngineering ;
```

### edo:ShackleThimble (line 16917)

```diff
-                   edo:hasDiscipline edo:SubseaRigidPipesEngineering ;
+                   edo:hasDiscipline edo:SubseaRigidPipesEngineering ,
+                                     edo:SubseaFlexiblePipesEngineering ;
```

### edo:Socket (line 17204)

```diff
-           edo:hasDiscipline edo:SubseaRigidPipesEngineering ;
+           edo:hasDiscipline edo:SubseaRigidPipesEngineering ,
+                             edo:SubseaFlexiblePipesEngineering ;
```

### edo:TrianglePlate (line 20076)

```diff
-                  edo:hasDiscipline edo:SubseaRigidPipesEngineering ;
+                  edo:hasDiscipline edo:SubseaRigidPipesEngineering ,
+                                    edo:SubseaFlexiblePipesEngineering ;
```

## Not modified

- **edo:TopBendStiffener** — already had `edo:SubseaFlexiblePipesEngineering`

## Updated (adição de disciplina)

### edo:VIVStrake (line 20642)

```diff
-              edo:hasDiscipline edo:SubseaRigidPipesEngineering ;
+              edo:hasDiscipline edo:SubseaRigidPipesEngineering ,
+                                edo:SubseaFlexiblePipesEngineering ;
```
