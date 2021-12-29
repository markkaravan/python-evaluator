class Transformer():
    def transformDefToLambda(self, defExp):
        [_, name, params, body] = defExp;
        return ['var', name, ['lambda', params, body]];
